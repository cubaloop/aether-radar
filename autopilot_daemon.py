"""Local helper loop. The CLOUD app already runs discovery/SEO/heartbeat on its own.
This local loop only handles WhatsApp outbound (needs this PC + paired WhatsApp)."""
import time, requests
from autonomous_prospector import run
PUBLIC = "https://aether-radar-nolb.onrender.com"
while True:
    try:
        print(time.strftime("%H:%M:%S"), "cloud status:", requests.get(PUBLIC + "/api/status", timeout=30).json())
    except Exception as e:
        print("cloud check failed:", e)
    try: run()
    except Exception as e: print("outbound error:", e)
    time.sleep(1800)
