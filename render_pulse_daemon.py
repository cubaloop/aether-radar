"""
AETHER RADAR — Render 24/7 Keep-Alive Heartbeat Pulse
Sends an HTTP ping to the public Render URL every 9 minutes
to prevent Render free tier from sleeping or idling.
"""
import time
import requests
import sys

TARGET_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8095"

print(f"[PULSE DAEMON] Initializing 24/7 wake-lock for: {TARGET_URL}")

while True:
    try:
        t0 = time.time()
        res = requests.get(f"{TARGET_URL}/api/config", timeout=15)
        latency = int((time.time() - t0) * 1000)
        print(f"[{time.strftime('%H:%M:%S')}] Heartbeat pulse sent to {TARGET_URL} | Status: {res.status_code} ({latency}ms)")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Heartbeat pulse warning: {e}")
    
    # Sleep 9 minutes (540 seconds) — Render sleeps at 15 minutes of idle
    time.sleep(540)
