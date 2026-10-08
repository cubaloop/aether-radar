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

# ─── Stealth Telemetry Sensor (Client Site Previews) ─────────────────────────
import json
TELEMETRY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "telemetry.json")
ADMIN_WHITELIST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "admin_whitelist.json")

def load_whitelist():
    if os.path.exists(ADMIN_WHITELIST_FILE):
        try:
            with open(ADMIN_WHITELIST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"ips": ["176.205.16.195"], "updated_at": None}

def save_whitelist(data):
    try:
        os.makedirs(os.path.dirname(ADMIN_WHITELIST_FILE), exist_ok=True)
        with open(ADMIN_WHITELIST_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        log.warning("whitelist save error: %s", e)

def load_telemetry():
    if os.path.exists(TELEMETRY_FILE):
        try:
            with open(TELEMETRY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_telemetry(data):
    try:
        os.makedirs(os.path.dirname(TELEMETRY_FILE), exist_ok=True)
        with open(TELEMETRY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        log.warning("telemetry save error: %s", e)

class TelemetryPing(BaseModel):
    slug: str
    session_id: str = ""
    event: str = "ping"  # 'enter', 'heartbeat', 'leave'
    duration_sec: int = 0
    device: str = ""
    is_admin: bool = False

@app.get("/admin/me", response_class=HTMLResponse)
async def admin_register_device(request: Request):
    ip = (request.headers.get("x-forwarded-for") or request.client.host).split(",")[0].strip()
    wl = load_whitelist()
    if ip not in wl["ips"]:
        wl["ips"].append(ip)
    wl["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save_whitelist(wl)
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Admin Whitelist | Aether Telemetry</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{ background: #080C0A; color: #F6F1E7; font-family: system-ui, sans-serif; }}
  </style>
</head>
<body class="min-h-screen flex items-center justify-center p-6">
  <div class="max-w-md w-full bg-[#121815] border border-[#C29B38]/40 rounded-3xl p-8 text-center shadow-2xl">
    <div class="w-16 h-16 rounded-2xl bg-[#C29B38]/20 border border-[#C29B38] text-[#ECC870] flex items-center justify-center mx-auto mb-6 text-3xl">
      🛡️
    </div>
    <h1 class="text-2xl font-bold mb-2 text-[#ECC870]">Administrador Registrado</h1>
    <p class="text-xs text-gray-300 mb-6">Tu IP y dispositivo han sido excluidos permanentemente del sensor espía.</p>
    
    <div class="bg-black/50 border border-gray-800 rounded-2xl p-4 text-left text-xs space-y-2 mb-6">
      <div class="flex justify-between">
        <span class="text-gray-400">IP Reconocida:</span>
        <span class="font-mono text-[#ECC870] font-semibold">{ip}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-400">Estado:</span>
        <span class="text-green-400 font-semibold">Excluido de Reportes</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-400">IPs en Whitelist:</span>
        <span class="text-gray-300">{len(wl['ips'])} registradas</span>
      </div>
    </div>
    
    <p class="text-[11px] text-gray-400 leading-relaxed mb-6">
      A partir de este momento puedes navegar por cualquier sitio de prueba sin que tus aperturas ni tiempo se sumen a las estadísticas de los clientes.
    </p>
    
    <a href="/" class="inline-block px-6 py-3 rounded-full bg-[#C29B38] hover:bg-[#A88228] text-black font-semibold text-xs tracking-wider uppercase transition-all">
      Volver al Sistema
    </a>
  </div>
  <script>
    localStorage.setItem('_aether_admin', '1');
    document.cookie = "_aether_admin=1; path=/; max-age=31536000";
  </script>
</body>
</html>"""
    response = HTMLResponse(content=html)
    response.set_cookie(key="_aether_admin", value="1", max_age=31536000, path="/")
    return response

@app.post("/api/telemetry/ping")
async def telemetry_ping(ping: TelemetryPing, request: Request):
    ip = (request.headers.get("x-forwarded-for") or request.client.host).split(",")[0].strip()
    wl = load_whitelist()
    is_admin = ping.is_admin or (ip in wl.get("ips", [])) or (request.cookies.get("_aether_admin") == "1")
    
    data = load_telemetry()
    slug = ping.slug.strip().lower()
    if slug not in data:
        data[slug] = {
            "slug": slug,
            "total_visits": 0,
            "sessions": {},
            "total_time_seconds": 0,
            "last_visit_at": None,
            "first_visit_at": None,
            "ips": []
        }
    
    entry = data[slug]
    now_iso = time.strftime("%Y-%m-%d %H:%M:%S")
    if not is_admin:
        if not entry.get("first_visit_at"):
            entry["first_visit_at"] = now_iso
        entry["last_visit_at"] = now_iso
        if ip not in entry["ips"]:
            entry["ips"].append(ip)

    sess_id = ping.session_id or f"{ip}_{int(time.time() // 3600)}"
    if sess_id not in entry["sessions"]:
        entry["sessions"][sess_id] = {
            "first_seen": now_iso,
            "last_seen": now_iso,
            "max_duration_sec": 0,
            "events_count": 0,
            "device": ping.device,
            "is_admin": is_admin
        }
        if not is_admin:
            entry["total_visits"] += 1
    
    sess = entry["sessions"][sess_id]
    sess["last_seen"] = now_iso
    sess["events_count"] += 1
    if is_admin:
        sess["is_admin"] = True
        
    if ping.duration_sec > sess["max_duration_sec"]:
        diff = ping.duration_sec - sess["max_duration_sec"]
        sess["max_duration_sec"] = ping.duration_sec
        if not is_admin:
            entry["total_time_seconds"] += diff
    
    save_telemetry(data)
    return {"ok": True, "admin": is_admin}

@app.get("/api/telemetry/stats")
async def telemetry_stats(include_admin: bool = False):
    data = load_telemetry()
    summary = {}
    for slug, info in data.items():
        client_sessions = [s for s in info.get("sessions", {}).values() if not s.get("is_admin", False)]
        client_time = sum(s.get("max_duration_sec", 0) for s in client_sessions)
        summary[slug] = {
            "total_visits": len(client_sessions),
            "unique_visitors": len([ip for ip in info.get("ips", []) if ip not in load_whitelist().get("ips", [])]),
            "total_time_seconds": client_time,
            "last_visit_at": info.get("last_visit_at"),
            "first_visit_at": info.get("first_visit_at"),
            "sessions_count": len(client_sessions),
            "admin_excluded_visits": len(info.get("sessions", {})) - len(client_sessions)
        }
    return {"status": "ok", "stats": summary, "raw": data if include_admin else {}}


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
