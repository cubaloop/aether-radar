"""
AETHER RADAR — 1-Click Public Deployment Helper
Exposes the local Aether Radar engine (running on http://localhost:8095)
to a global HTTPS public URL using built-in SSH or Localtunnel.
"""
import subprocess
import sys
import shutil

PORT = 8095

def deploy_via_ssh():
    print(f"\n[AETHER RADAR] Launching Global Tunnel via SSH (localhost.run)...")
    print(f"Forwarding localhost:{PORT} to public internet with automatic SSL...\n")
    cmd = ["ssh", "-R", f"80:localhost:{PORT}", "nokey@localhost.run"]
    subprocess.run(cmd)

def deploy_via_npx():
    print(f"\n[AETHER RADAR] Launching Global Tunnel via Localtunnel (npx)...")
    print(f"Forwarding localhost:{PORT} to public internet...\n")
    cmd = ["npx", "localtunnel", "--port", str(PORT)]
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    if shutil.which("ssh"):
        try:
            deploy_via_ssh()
        except KeyboardInterrupt:
            print("\nTunnel closed.")
    elif shutil.which("npx"):
        try:
            deploy_via_npx()
        except KeyboardInterrupt:
            print("\nTunnel closed.")
    else:
        print("Please install cloudflared or run: npx localtunnel --port 8095")

