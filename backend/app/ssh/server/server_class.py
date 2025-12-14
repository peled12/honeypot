import asyncssh

from app.ssh.server.auth import password_auth_handler
from app.ssh.server.session import HoneypotSSHSession

class HoneypotSSHServer(asyncssh.SSHServer):
    def connection_made(self, conn):
        self.conn = conn
        self.peername = conn.get_extra_info("peername")
        print(f"[ssh] connection from {self.peername}")

    def connection_lost(self, exc):
        print(f"[ssh] connection closed {getattr(self, 'peername', None)}")

    def begin_auth(self, username):
        return True # require password auth
    
    def password_auth_supported(self):
        return True # enable password auth and trigger validate_password
    
    def session_requested(self):
        return HoneypotSSHSession()
    
    def validate_password(self, username, password):
        # await the password auth handler
        print(f"[ssh.validate_password] username={username} password={password}")
        return password_auth_handler(self.conn, username, password)