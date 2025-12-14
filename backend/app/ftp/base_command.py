from app.ftp.connection import FTPConnection

# define the base command
class BaseCommand:
    """Base class for FTP commands."""
    async def handle(self, conn: FTPConnection, arg: str):
        raise NotImplementedError