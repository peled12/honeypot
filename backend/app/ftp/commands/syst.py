from app.ftp.base_command import BaseCommand
from app.ftp.connection import FTPConnection

class SystCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, arg: str):
        await conn.send("215 Windows Type: L8")
