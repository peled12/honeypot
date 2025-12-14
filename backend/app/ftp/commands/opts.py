from app.ftp.base_command import BaseCommand
from app.ftp.connection import FTPConnection

class OptsCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, arg: str):
        print(f"Connection from {conn.remote_ip}")
