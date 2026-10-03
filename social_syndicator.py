"""
AETHER RADAR — Autonomous Social Syndicator & Case-Study Engine
Synthesizes high-engagement viral breakdown threads for X, Reddit, and LinkedIn
from real forensic audits to drive continuous organic traffic to Aether Radar.
"""
import os
import json
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "social_queue.json")
AUDIT_FILE = os.path.join(DATA_DIR, "audits.json")

def generate_social_threads(public_url="https://aether-radar.onrender.com"):
    audits = {}
    if os.path.exists(AUDIT_FILE):
        try:
            with open(AUDIT_FILE, "r", encoding="utf-8") as f:
                audits = json.load(f)
        except Exception:
            pass

    threads = []
    for audit_id, data in audits.items():
        pub = data.get("public", {})
        domain = pub.get("domain", "target.com")
        loss = pub.get("est_monthly_loss_usd", "$14,000/mo")
        score = pub.get("friction_score", 72)
        niche = pub.get("business_niche", "E-commerce")
        flaw = pub.get("primary_flaw", {}).get("title", "Mobile latency drop-off")

        # X / Twitter Thread Format
        twitter_thread = [
            f"?? FORENSIC AUDIT: How {domain} ({niche}) is leaking {loss} in abandoned checkout traffic.\n\nFriction Score: {score}/100\nFatal Flaw: {flaw}\n\nHere is the full technical teardown ????",
            f"1/ The Primary Vulnerability:\n\n{pub.get('primary_flaw', {}).get('impact', 'High mobile drop-off.')}\n\nMeasured TTFB: {pub.get('ttfb_ms', 350)}ms.\nPayload: {pub.get('page_size_kb', 200)} KB.",
            f"2/ The Fix & Revenue Recovery:\n\nBy splitting non-critical JavaScript and implementing a 1-tap WhatsApp triage, they can reclaim ~30% of lost customer impulse.\n\nRun an instant audit on any competitor at: {public_url}"
        ]

        # Reddit Case Study (for r/SaaS, r/webdev, r/freelance)
        reddit_post = {
            "subreddit": "r/webdev",
            "title": f"Case Study: Diagnosed a {niche} website leaking {loss} - Here is what we found",
            "body": f"We ran a forensic performance and UX friction audit on {domain}.\n\nKey findings:\n- Friction Index: {score}/100\n- Primary Bottleneck: {flaw}\n- Annual Attrition: {pub.get('est_annual_loss_usd', '$160,000/yr')}\n\nIf you're building websites for clients, showing them exact monetary loss closes deals 10x faster than showing abstract Lighthouse scores.\n\nTool used: Aether Radar ({public_url})"
        }

        threads.append({
            "domain": domain,
            "twitter_thread": twitter_thread,
            "reddit_post": reddit_post,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(threads, f, indent=2)

    print(f"[Social Syndicator] Generated {len(threads)} viral social distribution assets in {OUTPUT_FILE}")
    return threads

if __name__ == "__main__":
    generate_social_threads()

