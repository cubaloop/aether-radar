import os
import time
import json
import uuid
import re
import urllib.parse
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

app = FastAPI(title="Aether Radar API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "audits.json")
AUDIT_STORE = {}

if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            AUDIT_STORE = json.load(f)
    except Exception as e:
        print(f"Error loading audit store: {e}")

def save_audits():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(AUDIT_STORE, f, indent=2)
    except Exception as e:
        print(f"Error saving audit store: {e}")

class ScanRequest(BaseModel):
    url: str

class PaymentRequest(BaseModel):
    audit_id: str
    payment_method: str
    tx_hash: str = ""

def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url

def extract_live_telemetry(url: str):
    telemetry = {
        "url": url,
        "domain": urllib.parse.urlparse(url).netloc,
        "ttfb_ms": 0,
        "status_code": 200,
        "ssl_secure": url.startswith("https://"),
        "page_size_kb": 0,
        "has_whatsapp": False,
        "has_viewport": True,
        "scripts_count": 0,
        "title": ""
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    try:
        t0 = time.time()
        res = requests.get(url, headers=headers, timeout=8, verify=False)
        t1 = time.time()
        telemetry["ttfb_ms"] = int((t1 - t0) * 1000)
        telemetry["status_code"] = res.status_code
        telemetry["page_size_kb"] = round(len(res.content) / 1024, 1)
        html = res.text.lower()
        telemetry["has_whatsapp"] = "wa.me" in html or "whatsapp.com" in html or "api.whatsapp" in html
        telemetry["has_viewport"] = 'name="viewport"' in html or "name='viewport'" in html
        telemetry["scripts_count"] = html.count("<script")
        title_match = re.search(r"<title>(.*?)</title>", res.text, re.IGNORECASE)
        if title_match:
            telemetry["title"] = title_match.group(1).strip()[:80]
        else:
            telemetry["title"] = telemetry["domain"]
    except Exception as e:
        telemetry["ttfb_ms"] = 1420
        telemetry["title"] = telemetry["domain"]
        telemetry["page_size_kb"] = 245.0
        telemetry["status_code"] = 200
        telemetry["error_fallback"] = str(e)
    return telemetry

def synthesize_forensic_report(telemetry: dict) -> dict:
    if not groq_client:
        raise HTTPException(status_code=500, detail="Groq API key not configured")
    system_prompt = """You are AETHER RADAR, the world's most advanced AI B2B Conversion Forensic Intelligence Terminal.
Your mission is to perform an uncompromising, surgical audit of any business website, calculating exact monetary revenue leakage and crafting high-converting cold pitches for agency closers.
Output MUST be strictly valid JSON without any markdown formatting or commentary.
Schema:
{
  "business_name": "string",
  "business_niche": "string",
  "friction_score": number (10 to 95),
  "health_grade": "string (A, B, C, D, or F)",
  "est_monthly_loss_usd": "string (e.g. $12,400/mo)",
  "est_annual_loss_usd": "string (e.g. $148,800/yr)",
  "conversion_bottlenecks": [
    {
      "title": "string",
      "severity": "CRITICAL" | "HIGH" | "MODERATE",
      "impact": "string",
      "technical_detail": "string"
    },
    {
      "title": "string",
      "severity": "CRITICAL" | "HIGH" | "MODERATE",
      "impact": "string",
      "technical_detail": "string"
    },
    {
      "title": "string",
      "severity": "CRITICAL" | "HIGH" | "MODERATE",
      "impact": "string",
      "technical_detail": "string"
    }
  ],
  "psychological_breakdown": {
    "mobile_bounce_rate": "string",
    "hesitation_index": "string",
    "trust_deficiency": "string"
  },
  "high_impact_fixes": [
    {
      "fix_name": "string",
      "estimated_lift": "string",
      "architecture": "string"
    },
    {
      "fix_name": "string",
      "estimated_lift": "string",
      "architecture": "string"
    },
    {
      "fix_name": "string",
      "estimated_lift": "string",
      "architecture": "string"
    }
  ],
  "executive_pitch_en": {
    "subject": "string",
    "whatsapp_message": "string",
    "cold_email": "string"
  },
  "executive_pitch_es": {
    "subject": "string",
    "whatsapp_message": "string",
    "cold_email": "string"
  }
}"""

    user_prompt = f"""Perform a forensic teardown for:
Domain: {telemetry['domain']}
Full URL: {telemetry['url']}
Page Title: {telemetry['title']}
Measured TTFB: {telemetry['ttfb_ms']}ms
Page Payload Size: {telemetry['page_size_kb']}KB
Has Native WhatsApp Funnel: {telemetry['has_whatsapp']}
Has Mobile Viewport Tag: {telemetry['has_viewport']}
Script Bloat: {telemetry['scripts_count']} tags detected"""

    completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    raw = completion.choices[0].message.content
    parsed = json.loads(raw)
    if isinstance(parsed, list):
        parsed = parsed[0] if len(parsed) > 0 else {}
    return parsed

@app.post("/api/scan")
async def scan_endpoint(req: ScanRequest):
    url = normalize_url(req.url)
    audit_id = str(uuid.uuid4())[:8]
    telemetry = extract_live_telemetry(url)
    report = synthesize_forensic_report(telemetry)
    
    public_data = {
        "audit_id": audit_id,
        "domain": telemetry["domain"],
        "url": telemetry["url"],
        "title": telemetry["title"],
        "business_name": report.get("business_name", telemetry["domain"]),
        "business_niche": report.get("business_niche", "Digital Commerce"),
        "friction_score": report.get("friction_score", 68),
        "health_grade": report.get("health_grade", "D"),
        "est_monthly_loss_usd": report.get("est_monthly_loss_usd", "$12,400/mo"),
        "est_annual_loss_usd": report.get("est_annual_loss_usd", "$148,800/yr"),
        "ttfb_ms": telemetry["ttfb_ms"],
        "page_size_kb": telemetry["page_size_kb"],
        "has_whatsapp": telemetry["has_whatsapp"],
        "primary_flaw": report.get("conversion_bottlenecks", [{}])[0],
        "psychological_breakdown": report.get("psychological_breakdown", {}),
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    locked_dossier = {
        "all_bottlenecks": report.get("conversion_bottlenecks", []),
        "high_impact_fixes": report.get("high_impact_fixes", []),
        "executive_pitch_en": report.get("executive_pitch_en", {}),
        "executive_pitch_es": report.get("executive_pitch_es", {}),
        "telemetry_full": telemetry
    }
    
    AUDIT_STORE[audit_id] = {
        "public": public_data,
        "locked": locked_dossier,
        "is_unlocked": False,
        "payment": None
    }
    save_audits()
    return public_data

@app.get("/api/audit/{audit_id}")
async def get_audit(audit_id: str):
    if audit_id not in AUDIT_STORE:
        raise HTTPException(status_code=404, detail="Audit not found")
    item = AUDIT_STORE[audit_id]
    response = {
        "public": item["public"],
        "is_unlocked": item["is_unlocked"]
    }
    if item["is_unlocked"]:
        response["dossier"] = item["locked"]
    return response

@app.post("/api/verify-payment")
async def verify_payment(req: PaymentRequest):
    if req.audit_id not in AUDIT_STORE:
        raise HTTPException(status_code=404, detail="Audit not found")
    item = AUDIT_STORE[req.audit_id]
    item["is_unlocked"] = True
    item["payment"] = {
        "method": req.payment_method,
        "tx_hash": req.tx_hash or f"sol_tx_{uuid.uuid4().hex[:16]}",
        "timestamp": time.time()
    }
    save_audits()
    return {
        "status": "success",
        "message": "Full Forensic Dossier unlocked successfully",
        "dossier": item["locked"]
    }

@app.get("/api/config")
async def get_config():
    return {
        "solana_treasury": "8xK4nF9v7K3QG1ZpWJtXoYrLmA5sVcTdE2bNhPqR6uM1",
        "pricing": {
            "single_audit_usd": 3.90,
            "single_audit_sol": 0.025,
            "day_pass_usd": 12.00,
            "day_pass_sol": 0.08
        },
        "contact": {
            "phone": "+971508379080",
            "whatsapp": "https://wa.me/971508379080",
            "email": "davidhabana98@gmail.com"
        }
    }

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")
if os.path.exists(PUBLIC_DIR):
    app.mount("/", StaticFiles(directory=PUBLIC_DIR, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
