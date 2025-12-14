# handles pass command
from app.ftp.connection import FTPConnection
from app.ftp.base_command import BaseCommand


class PassCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, arg: str):
        if conn.username is not None:
            conn.logged_in = True
            await conn.send("230 Login successful")
        else: # ensure USER is sent first
            await conn.send("503 Login with USER first")
