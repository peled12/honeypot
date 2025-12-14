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


class TestSSHServer(asyncssh.SSHServer):
    def password_auth_supported(self):
        return True
    def validate_password(self, username, password):
        print(f"Auth: {username} / {password}")
        return True

class DebugSession(asyncssh.SSHServerSession):
    def __init__(self, *args, **kwargs):
        print("[SESSION] __init__")

    def connection_made(self, chan):
        try:
            print("[SESSION] connection_made", chan)
            self._chan = chan
        except Exception as e:
            print("[SESSION] connection_made EXC:", e)
            raise

    def pty_requested(self, term, w, h, pw, ph, modes):
        print("[SESSION] pty_requested", term, w, h)
        return True

    def shell_requested(self):
        print("[SESSION] shell_requested")
        try:
            self._chan.write("Welcome!\n$ ")
            return True
        except Exception as e:
            print("[SESSION] shell_requested EXC:", e)
            return False

    def exec_requested(self, command):
        print("[SESSION] exec_requested:", command)
        try:
            self._chan.write(f"Fake exec: {command}\n")
            self._chan.exit(0)
            return True
        except Exception as e:
            print("[SESSION] exec_requested EXC:", e)
            return False

    def data_received(self, data, datatype):
        print("[SESSION] data_received:", data)
        self._chan.write(data + "\n$ ")

    def connection_lost(self, exc):
        print("[SESSION] connection_lost", exc)
