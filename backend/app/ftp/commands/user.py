from app.ftp.connection import FTPConnection
from app.ftp.base_command import BaseCommand

# handles user command
class UserCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, arg: str):
        conn.username = arg
        await conn.send("331 Username OK, need password")
