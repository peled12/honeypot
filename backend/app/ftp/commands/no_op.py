from app.ftp.connection import FTPConnection
from app.ftp.base_command import BaseCommand

# handles no-op command
class NoOpCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, arg: str):
        await conn.send("502 Command not implemented")