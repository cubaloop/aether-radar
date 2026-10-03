"""Stateless Solana Pay (USDC) verification. No database: dossier is sealed in a token,
and each audit has a unique on-chain reference derived from a server secret."""
import os, hmac, hashlib, base64, json, requests
from cryptography.fernet import Fernet, InvalidToken

A = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

def b58(b):
    n = int.from_bytes(b, "big"); s = b""
    while n:
        n, r = divmod(n, 58); s = A[r:r+1] + s
    return (A[0:1] * (len(b) - len(b.lstrip(b"\0"))) + s).decode()

def cfg():
    return {"secret": os.getenv("AETHER_SECRET", ""), "treasury": os.getenv("TREASURY_ADDRESS", ""),
            "price": float(os.getenv("PRICE_USDC", "3.90")),
            "rpc": os.getenv("SOLANA_RPC", "https://api.mainnet-beta.solana.com")}

def _f():
    return Fernet(base64.urlsafe_b64encode(hashlib.sha256(cfg()["secret"].encode()).digest()))

def seal(obj):
    return _f().encrypt(json.dumps(obj).encode()).decode()

def unseal(tok, ttl=7 * 86400):
    try:
        return json.loads(_f().decrypt(tok.encode(), ttl=ttl))
    except (InvalidToken, Exception):
        return None

def reference(audit_id):
    return b58(hmac.new(cfg()["secret"].encode(), b"ref:" + audit_id.encode(), hashlib.sha256).digest())

def pay_info(audit_id):
    c = cfg(); ref = reference(audit_id)
    uri = ("solana:%s?amount=%s&spl-token=%s&reference=%s&label=Aether%%20Radar&message=Audit%%20%s"
           % (c["treasury"], c["price"], USDC, ref, audit_id))
    return {"uri": uri, "treasury": c["treasury"], "amount": c["price"], "mint": USDC, "reference": ref}

def _rpc(method, params):
    r = requests.post(cfg()["rpc"], json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, timeout=20)
    return r.json().get("result")

def verify(audit_id):
    c = cfg(); ref = reference(audit_id)
    sigs = _rpc("getSignaturesForAddress", [ref, {"limit": 10, "commitment": "confirmed"}]) or []
    for s in sigs:
        if s.get("err"):
            continue
        tx = _rpc("getTransaction", [s["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0, "commitment": "confirmed"}])
        meta = (tx or {}).get("meta") or {}
        if meta.get("err"):
            continue
        def bal(lst):
            return sum(float(b["uiTokenAmount"].get("uiAmountString") or 0) for b in (lst or [])
                       if b.get("mint") == USDC and b.get("owner") == c["treasury"])
        delta = bal(meta.get("postTokenBalances")) - bal(meta.get("preTokenBalances"))
        if delta >= c["price"] - 0.001:
            return True, s["signature"]
    return False, None
