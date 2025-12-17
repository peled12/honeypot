from app.ftp.base_command import BaseCommand
from app.ftp.connection import FTPConnection


class PwdCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, arg):
        await conn.send(f'257 "{conn.cwd}" is current directory')
