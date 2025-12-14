# handles quit command
from app.ftp.connection import FTPConnection
from app.ftp.base_command import BaseCommand


class QuitCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, arg: str):
        await conn.send("221 Goodbye")
        await conn.close()