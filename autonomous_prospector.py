"""Outbound via the user's own gmaps-lead-gen leads + Baileys gateway.
Only sends when WhatsApp is actually connected. Facts only, no invented numbers. Max per day capped."""
import os, json, time, sqlite3, requests
from dotenv import load_dotenv
load_dotenv()
import core

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.getenv("LEADS_DB", r"C:\Users\Yo\.gemini\antigravity\scratch\gmaps-lead-gen\backend\leads.db")
GATEWAY = os.getenv("WA_GATEWAY", "http://localhost:3001")
PUBLIC = os.getenv("PUBLIC_URL", "https://aether-radar-nolb.onrender.com").rstrip("/")
LOG = os.path.join(HERE, "data", "outbound_log.json")
STATE = os.path.join(HERE, "data", "outbound_status.json")
MAX_PER_DAY = int(os.getenv("OUTBOUND_MAX_PER_DAY", "10"))
os.makedirs(os.path.join(HERE, "data"), exist_ok=True)

def load(p, d):
    try: return json.load(open(p, encoding="utf-8"))
    except Exception: return d

def gateway_connected():
    try:
        s = requests.get(GATEWAY + "/status", timeout=4).json()
        return bool(s.get("connected") or s.get("isConnected") or s.get("status") == "connected"), s
    except Exception as e:
        return False, {"error": "gateway offline: %s" % type(e).__name__}

def leads():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
    rows = c.execute("select name,formatted_phone,website,category,city from leads where has_website=1 "
                     "and formatted_phone is not null and website is not null").fetchall()
    return [dict(r) for r in rows]

def message(l, pub):
    wa = "no WhatsApp click-to-chat button" if not pub["has_whatsapp"] else "a WhatsApp button"
    return ("Hi %s team, I ran an automated check on %s: homepage responds in %s ms (%s KB) and has %s. "
            "Rough modeled estimate of revenue at risk: %s (assumptions stated in the report). "
            "Free interactive breakdown: %s/?scan=%s - happy to explain the fixes, no obligation."
            % (l["name"], l["website"], pub["ttfb_ms"], pub["page_size_kb"], wa, pub["est_monthly_loss_usd"], PUBLIC, core.norm_domain(l["website"])))

def run():
    ok, st = gateway_connected()
    state = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "gateway_connected": ok, "detail": st}
    sent_log = load(LOG, [])
    today = time.strftime("%Y-%m-%d")
    sent_today = sum(1 for x in sent_log if x["date"] == today)
    if not ok:
        state["blocked"] = "WhatsApp not connected - one-time QR pairing required at %s/qr" % GATEWAY
        json.dump(state, open(STATE, "w"), indent=2); print(state["blocked"]); return
    done = {x["phone"] for x in sent_log}
    for l in leads():
        if sent_today >= MAX_PER_DAY: break
        if l["formatted_phone"] in done: continue
        dom = core.norm_domain(l["website"])
        if not dom: continue
        if dom in {"tiktok.com", "instagram.com", "facebook.com", "google.com", "youtube.com", "twitter.com", "x.com", "linkedin.com", "linktr.ee", "whatsapp.com"}:
            continue
        pub, _, _ = core.analyze(dom)
        if not pub: continue
        r = requests.post(GATEWAY + "/send", json={"to": l["formatted_phone"], "message": message(l, pub)}, timeout=30)
        res = r.json() if r.ok else {"success": False}
        is_success = bool(res.get("success"))
        sent_log.append({"date": today, "phone": l["formatted_phone"], "name": l["name"], "domain": dom,
                         "success": is_success, "detail": res.get("error") or "delivered", "time": time.strftime("%H:%M:%S")})
        json.dump(sent_log, open(LOG, "w"), indent=2)
        if is_success:
            sent_today += 1
            time.sleep(45)
    state["sent_today"] = sent_today
    json.dump(state, open(STATE, "w"), indent=2)

if __name__ == "__main__":
    run()
