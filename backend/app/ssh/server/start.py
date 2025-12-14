import os
import asyncio
import asyncssh

import logging
logging.basicConfig(level=logging.DEBUG)
asyncssh.set_debug_level(2)


from .server_class import HoneypotSSHServer
from .session import HoneypotSSHSession

# starts the ssh honeypot server
async def start_ssh_server(
    host: str = "0.0.0.0",
    port: int = 2222,
    host_key_path: str = None
):
    host_key_path = host_key_path or os.getenv("SSH_HOST_KEY", "./host_key")

    print(f"[ssh] Starting SSH honeypot on {host}:{port}, host key: {host_key_path}")

    # bind a socket and start accepting connections
    await asyncssh.create_server(
        HoneypotSSHServer,
        host,
        port,
        server_host_keys=[host_key_path],
    )

    # keep the server running
    await asyncio.Event().wait()