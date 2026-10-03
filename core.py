"""Aether Radar core: real telemetry + LLM analysis. No fabricated fallback data."""
import os, re, json, time, uuid, urllib.parse, requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from groq import Groq

MODEL = "openai/gpt-oss-120b"
_client = None

def client():
    global _client
    if _client is None:
        k = os.getenv("GROQ_API_KEY")
        if not k:
            raise RuntimeError("GROQ_API_KEY missing")
        _client = Groq(api_key=k)
    return _client

def llm_json(system, user, temperature=0.2):
    c = client().chat.completions.create(
        model=MODEL, temperature=temperature, response_format={"type": "json_object"},
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
    d = json.loads(c.choices[0].message.content)
    if isinstance(d, list):
        d = d[0] if d else {}
    return d

DOM_RE = re.compile(r"^(?=.{4,100}$)([a-z0-9-]+\.)+[a-z]{2,}$")

def norm_domain(raw):
    raw = (raw or "").strip().lower()
    raw = re.sub(r"^https?://", "", raw).split("/")[0].split("?")[0].split(":")[0]
    raw = re.sub(r"^www\.", "", raw)
    return raw if DOM_RE.match(raw) else None

def telemetry(domain):
    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
    t = {"domain": domain, "url": "https://" + domain, "reachable": False}
    try:
        r = requests.get(t["url"], headers=h, timeout=12, verify=False, allow_redirects=True)
    except Exception as e:
        t["error"] = str(e)[:120]
        return t
    html = r.text.lower()
    m = re.search(r"<title[^>]*>(.*?)</title>", r.text, re.I | re.S)
    t.update(reachable=r.status_code < 400, status=r.status_code,
             ttfb_ms=int(r.elapsed.total_seconds() * 1000),
             page_size_kb=round(len(r.content) / 1024, 1),
             scripts=html.count("<script"),
             has_whatsapp=("wa.me" in html or "api.whatsapp.com" in html or "whatsapp.com/send" in html),
             has_viewport=("name=\"viewport\"" in html or "name='viewport'" in html),
             title=(m.group(1).strip()[:90] if m else domain), https=r.url.startswith("https://"))
    return t

SYSTEM = """You are a website conversion analyst. You receive REAL measured data about a website. Base every diagnosis ONLY on the measured data and on the business type implied by the domain/title. Do NOT invent statistics, study results, or reply rates.
Return strict JSON:
{"business_name":str,"business_niche":str,"friction_score":int 10-95,"health_grade":"A|B|C|D|F",
"est_monthly_loss_usd":"conservative RANGE string like $1,500-$4,000/mo","est_annual_loss_usd":"range string like $18,000-$48,000/yr",
"loss_assumptions":"one sentence stating the modeling assumptions (e.g. traffic assumed, conversion impact of measured load time/missing WhatsApp)",
"conversion_bottlenecks":[{"title":str,"severity":"CRITICAL|HIGH|MODERATE","impact":str,"technical_detail":str}] (exactly 3),
"psychological_breakdown":{"mobile_bounce_rate":str,"hesitation_index":str,"trust_deficiency":str},
"high_impact_fixes":[{"fix_name":str,"estimated_lift":str,"architecture":str}] (exactly 3),
"executive_pitch_en":{"subject":str,"whatsapp_message":str,"cold_email":str},
"executive_pitch_es":{"subject":str,"whatsapp_message":str,"cold_email":str}}
Label all money figures as estimates. Keep the pitches honest, specific to the measured data, and free of fake guarantees."""

def analyze(domain):
    t = telemetry(domain)
    if not t["reachable"]:
        return None, None, t
    user = ("Domain: %s\nTitle: %s\nHTTP status: %s\nResponse time (headers): %s ms\nHTML size: %s KB\n"
            "Script tags: %s\nWhatsApp click-to-chat link present: %s\nMobile viewport meta: %s\nHTTPS: %s" %
            (t["domain"], t["title"], t["status"], t["ttfb_ms"], t["page_size_kb"], t["scripts"],
             t["has_whatsapp"], t["has_viewport"], t["https"]))
    r = llm_json(SYSTEM, user)
    bn = r.get("conversion_bottlenecks") or [{}]
    aid = uuid.uuid4().hex[:10]
    public = {
        "audit_id": aid, "domain": domain, "url": t["url"], "title": t["title"],
        "business_name": r.get("business_name", domain), "business_niche": r.get("business_niche", "Business"),
        "friction_score": r.get("friction_score", 60), "health_grade": r.get("health_grade", "C"),
        "est_monthly_loss_usd": r.get("est_monthly_loss_usd", "n/a"), "est_annual_loss_usd": r.get("est_annual_loss_usd", "n/a"),
        "loss_assumptions": r.get("loss_assumptions", ""),
        "ttfb_ms": t["ttfb_ms"], "page_size_kb": t["page_size_kb"], "has_whatsapp": t["has_whatsapp"],
        "primary_flaw": bn[0], "psychological_breakdown": r.get("psychological_breakdown", {}),
        "created_at": time.strftime("%Y-%m-%d")}
    locked = {"all_bottlenecks": bn, "high_impact_fixes": r.get("high_impact_fixes", []),
              "executive_pitch_en": r.get("executive_pitch_en", {}), "executive_pitch_es": r.get("executive_pitch_es", {}),
              "telemetry_full": t}
    return public, locked, t
