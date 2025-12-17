from app.ftp.base_command import BaseCommand
from app.ftp.connection import FTPConnection

class TypeCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, arg):
        if arg in ["I", "A"]:
            await conn.send(f"200 Type set to {arg}")
        else:
            await conn.send("504 Command not implemented for that type")
