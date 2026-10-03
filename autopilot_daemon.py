"""
AETHER RADAR — Master Autopilot Daemon
Coordinates autonomous lead prospecting, social syndication, and system health
with zero human intervention.
"""
import time
import os
import json
import requests
from autonomous_prospector import run_prospecting_sprint
from social_syndicator import generate_social_threads

STATUS_FILE = os.path.join(os.path.dirname(__file__), "data", "daemon_status.json")

def update_status(event):
    status = {
        "status": "RUNNING",
        "last_event": event,
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2)

def run_autopilot_cycle():
    print(f"\n[{time.strftime('%H:%M:%S')}] === STARTING AUTOPILOT CYCLE ===")
    
    # 1. Verify Aether Radar Server Health
    try:
        res = requests.get("http://localhost:8095/api/config", timeout=5)
        if res.status_code == 200:
            print("[HEALTH] Aether Radar API is online and responding.")
        else:
            print(f"[HEALTH WARNING] API returned status {res.status_code}")
    except Exception as e:
        print(f"[HEALTH ALERT] Aether Radar API offline: {e}")

    # 2. Run Prospecting Sprint
    try:
        run_prospecting_sprint(max_targets=2)
        update_status("Completed autonomous prospecting sprint")
    except Exception as e:
        print(f"[PROSPECTOR ERROR] {e}")

    # 3. Update Social Distribution Queue
    try:
        generate_social_threads()
        update_status("Generated fresh social breakdown assets")
    except Exception as e:
        print(f"[SYNDICATOR ERROR] {e}")

    print(f"[{time.strftime('%H:%M:%S')}] === AUTOPILOT CYCLE COMPLETE ===")

if __name__ == "__main__":
    print("[AETHER RADAR AUTOPILOT] Initializing 24/7 autonomous growth daemon...")
    run_autopilot_cycle()

