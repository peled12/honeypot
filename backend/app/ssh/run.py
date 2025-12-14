import os
import asyncio
from app.ssh.server.start import start_ssh_server

if __name__ == "__main__":
    host = os.getenv("SSH_HOST", "0.0.0.0")
    port = int(os.getenv("SSH_PORT", "2222"))
    host_key = os.getenv("SSH_HOST_KEY", "/app/host_key")

    print(f"[ssh.run] Starting SSH honeypot on {host}:{port}, host key: {host_key}")
    asyncio.run(start_ssh_server(host=host, port=port, host_key_path=host_key))
