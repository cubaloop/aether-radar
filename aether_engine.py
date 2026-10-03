import os, time, asyncio, logging
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import core, solana_pay, seo

log = logging.getLogger("aether")
app = FastAPI(title="Aether Radar", version="2.0")
DAILY_CAP = int(os.getenv("DAILY_LLM_CAP", "400"))
_hits = defaultdict(list)
_day = {"d": time.strftime("%Y-%m-%d"), "n": 0}

def budget_ok():
    d = time.strftime("%Y-%m-%d")
    if _day["d"] != d:
        _day.update(d=d, n=0)
    if _day["n"] >= DAILY_CAP:
        return False
    _day["n"] += 1
    return True

class Scan(BaseModel):
    url: str

class Tok(BaseModel):
    token: str

@app.get("/healthz")
async def healthz():
    return {"ok": True}

@app.get("/api/config")
async def config():
    c = solana_pay.cfg()
    return {"pricing": {"audit_usdc": c["price"]}, "treasury": c["treasury"], "demo": False,
            "contact": {"phone": "+971508379080", "whatsapp": "https://wa.me/971508379080", "email": "davidhabana98@gmail.com"}}

@app.post("/api/scan")
async def scan(req: Scan, request: Request):
    ip = (request.headers.get("x-forwarded-for") or request.client.host).split(",")[0].strip()
    now = time.time(); _hits[ip] = [t for t in _hits[ip] if now - t < 3600]
    if len(_hits[ip]) >= 8:
        raise HTTPException(429, "Rate limit: 8 audits per hour per visitor.")
    d = core.norm_domain(req.url)
    if not d:
        raise HTTPException(422, "Enter a valid domain, e.g. example.com")
    if not budget_ok():
        raise HTTPException(503, "Daily capacity reached. Try again tomorrow.")
    _hits[ip].append(now)
    pub, locked, t = await asyncio.to_thread(core.analyze, d)
    if not pub:
        raise HTTPException(422, "Could not reach %s. Check the domain and try again." % d)
    pub["token"] = solana_pay.seal({"aid": pub["audit_id"], "locked": locked})
    return pub

@app.post("/api/pay-info")
async def pay_info(req: Tok):
    s = solana_pay.unseal(req.token)
    if not s:
        raise HTTPException(400, "Invalid or expired audit token")
    return solana_pay.pay_info(s["aid"])

@app.post("/api/verify-payment")
async def verify_payment(req: Tok):
    s = solana_pay.unseal(req.token)
    if not s:
        raise HTTPException(400, "Invalid or expired audit token")
    ok, sig = await asyncio.to_thread(solana_pay.verify, s["aid"])
    if not ok:
        return {"status": "pending"}
    return {"status": "success", "tx": sig, "dossier": s["locked"]}

@app.get("/report/{domain}", response_class=HTMLResponse)
async def report(domain: str):
    d = core.norm_domain(domain)
    p = seo.get_report(d) if d else None
    if not p:
        raise HTTPException(404, "No audit published for this domain yet")
    return HTMLResponse(seo.render_page(p))

@app.get("/reports", response_class=HTMLResponse)
async def reports():
    items = "".join('<li><a href="/report/%s">%s</a></li>' % (d, d) for d in seo.list_reports())
    return HTMLResponse("<!doctype html><title>Website audits | Aether Radar</title><body style='font:16px system-ui;background:#070b16;color:#e6edf6;padding:40px'>"
                        "<h1>Published website audits</h1><ul>%s</ul><p><a style='color:#4ee0ff' href='/'>Audit your own site</a></p></body>" % items)

@app.get("/sitemap.xml")
async def sitemap():
    return Response(seo.sitemap(), media_type="application/xml")

@app.get("/robots.txt")
async def robots():
    return PlainTextResponse("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % seo.public_url())

@app.get("/{key}.txt")
async def indexnow_key(key: str):
    if key == seo.indexnow_key():
        return PlainTextResponse(key)
    raise HTTPException(404)

@app.get("/api/status")
async def status():
    return {"targets": len(seo.load_targets()["domains"]), "reports": len(seo.list_reports()), "llm_calls_today": _day["n"]}

async def autopilot():
    """Runs inside Render: self-heartbeat + discovery + SEO report generation + IndexNow. No PC required."""
    await asyncio.sleep(15)
    while True:
        try:
            await asyncio.to_thread(requests.get, seo.public_url() + "/healthz", timeout=20)
            t = seo.load_targets()
            if len(t["domains"]) - len(seo.list_reports()) < 8 and budget_ok():
                await asyncio.to_thread(seo.discover_batch)
                t = seo.load_targets()
            done = set(seo.list_reports()); new = []
            for d in t["domains"]:
                if d in done:
                    continue
                if len(new) >= 6 or not budget_ok():
                    break
                if await asyncio.to_thread(seo.build_report, d):
                    new.append(d)
                await asyncio.sleep(3)
            if new:
                log.warning("IndexNow %s for %d new reports", await asyncio.to_thread(seo.indexnow_submit, new), len(new))
        except Exception as e:
            log.warning("autopilot error: %s", e)
        await asyncio.sleep(540)

@app.on_event("startup")
async def _start():
    asyncio.create_task(autopilot())

PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
app.mount("/", StaticFiles(directory=PUBLIC_DIR, html=True), name="static")
