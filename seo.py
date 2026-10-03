"""Programmatic SEO + discovery. Everything here runs inside the cloud app (no PC needed)."""
import os, json, time, hmac, hashlib, html, requests
import core

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
REP = os.path.join(DATA, "reports")
os.makedirs(REP, exist_ok=True)
TARGETS_F = os.path.join(DATA, "targets.json")
NICHES = ["luxury car rental", "aesthetic clinic", "dental clinic", "real estate agency", "yacht charter",
          "interior design studio", "wedding photographer", "private jet charter", "spa and wellness center",
          "law firm", "restaurant group", "furniture store", "jewelry boutique", "private school", "travel agency"]
CITIES = ["Dubai", "Abu Dhabi", "London", "Miami", "Riyadh", "Doha"]

def public_url():
    return os.getenv("PUBLIC_URL", "http://localhost:8095").rstrip("/")

def load_targets():
    try:
        return json.load(open(TARGETS_F, encoding="utf-8"))
    except Exception:
        return {"domains": [], "cursor": 0}

def save_targets(t):
    json.dump(t, open(TARGETS_F, "w", encoding="utf-8"))

def discover_batch():
    """Ask the LLM for candidate domains, KEEP ONLY those that really respond over HTTPS."""
    t = load_targets()
    n = t["cursor"]; niche = NICHES[n % len(NICHES)]; city = CITIES[(n // len(NICHES)) % len(CITIES)]
    t["cursor"] = n + 1
    out = core.llm_json("Return JSON {\"domains\":[...]} with 25 real business website domains (no URLs, no paths).",
                        "Real, well-known independent %s businesses in %s." % (niche, city), 0.5)
    added = 0
    for d in out.get("domains", []):
        d = core.norm_domain(str(d))
        if not d or d in t["domains"]:
            continue
        if core.telemetry(d).get("reachable"):
            t["domains"].append(d); added += 1
    save_targets(t)
    return added

def report_path(d):
    return os.path.join(REP, d + ".json")

def get_report(d):
    try:
        return json.load(open(report_path(d), encoding="utf-8"))
    except Exception:
        return None

def build_report(d):
    pub, _locked, _t = core.analyze(d)
    if not pub:
        return None
    json.dump(pub, open(report_path(d), "w", encoding="utf-8"))
    return pub

def list_reports():
    return sorted(f[:-5] for f in os.listdir(REP) if f.endswith(".json"))

def _e(x):
    return html.escape(str(x))

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="article">
<style>body{{margin:0;font:16px/1.6 system-ui,Segoe UI,sans-serif;color:#e6edf6;background:radial-gradient(at 0 0,#12304f,transparent 55%),radial-gradient(at 100% 100%,#2a1550,transparent 55%),#070b16}}
main{{max-width:820px;margin:0 auto;padding:48px 20px}}a{{color:#4ee0ff}}.card{{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:22px;margin:18px 0}}
.k{{display:flex;gap:14px;flex-wrap:wrap}}.k div{{flex:1;min-width:150px}}.k b{{display:block;font-size:26px}}small,.muted{{color:#93a4bb}}
.btn{{display:inline-block;background:linear-gradient(90deg,#06b6d4,#2563eb);color:#021;font-weight:800;padding:14px 22px;border-radius:12px;text-decoration:none}}</style></head>
<body><main><p><a href="/">Aether Radar</a> / <a href="/reports">Website audits</a></p>
<h1>{name}: website audit ({domain})</h1>
<p class="muted">Automated analysis of the public homepage, generated {date}. Measured values below are real; money figures are modeled estimates, not the company's actual revenue.</p>
<div class="card k"><div><small>Friction score</small><b>{score}/100</b>Grade {grade}</div><div><small>Response time</small><b>{ttfb} ms</b></div>
<div><small>HTML size</small><b>{size} KB</b></div><div><small>WhatsApp click-to-chat</small><b>{wa}</b></div></div>
<div class="card"><small>Estimated monthly revenue at risk (model)</small><h2>{loss}</h2><p class="muted">{assump}</p><p class="muted" style="font-size:11px;border-left:2px solid #06b6d4;padding-left:8px;margin-top:8px;">Disclaimer: Cifras de pérdida estimadas mediante simulación de coste de oportunidad y benchmarks de conversión por latencia técnica; no constituyen registros contables ni analíticas privadas.</p></div>
<div class="card"><small>Primary issue ({sev})</small><h3>{flaw}</h3><p>{impact}</p></div>
<p class="muted">Own this site or sell web services? The full dossier includes all 3 fixes and ready-to-send outreach copy.</p>
</main></body></html>"""

def render_page(p):
    f = p.get("primary_flaw") or {}
    return PAGE.format(
        title=_e("%s website audit: %s/100 friction score | Aether Radar" % (p["business_name"], p["friction_score"])),
        desc=_e("Measured load time %s ms, %s KB. Primary issue: %s." % (p["ttfb_ms"], p["page_size_kb"], f.get("title", "n/a"))),
        url=_e("%s/report/%s" % (public_url(), p["domain"])), name=_e(p["business_name"]), domain=_e(p["domain"]),
        date=_e(p.get("created_at", "")), score=_e(p["friction_score"]), grade=_e(p["health_grade"]),
        ttfb=_e(p["ttfb_ms"]), size=_e(p["page_size_kb"]), wa="Yes" if p.get("has_whatsapp") else "Missing",
        loss=_e(p["est_monthly_loss_usd"]), assump=_e(p.get("loss_assumptions", "")),
        sev=_e(f.get("severity", "")), flaw=_e(f.get("title", "")), impact=_e(f.get("impact", "")))

def sitemap():
    u = public_url()
    urls = [u + "/", u + "/reports"] + ["%s/report/%s" % (u, d) for d in list_reports()]
    return ('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
            "".join("<url><loc>%s</loc></url>" % _e(x) for x in urls) + "</urlset>")

def indexnow_key():
    return hmac.new(os.getenv("AETHER_SECRET", "x").encode(), b"indexnow", hashlib.sha256).hexdigest()[:32]

def indexnow_submit(domains):
    if not domains or public_url().startswith("http://localhost"):
        return None
    u = public_url(); host = u.split("//")[1]
    body = {"host": host, "key": indexnow_key(), "keyLocation": "%s/%s.txt" % (u, indexnow_key()),
            "urlList": ["%s/report/%s" % (u, d) for d in domains][:9000]}
    r = requests.post("https://api.indexnow.org/indexnow", json=body, timeout=20)
    return r.status_code
