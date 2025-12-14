import asyncio
from app.ftp.db_utild import save_event_background
from app.ftp.connection import FTPConnection
from app.ftp.base_command import BaseCommand
from app.schemas import EventCreate

# handles stor command
class StorCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, filename: str):
        if not conn.logged_in:
            await conn.send("530 Not logged in")
            return
        await conn.send("150 Opening data connection for file upload")

        file_bytes = await conn.read_data_socket() # read data

        # logs the event only here for stor command
        event_obj = await EventCreate.from_ftp(
            src_ip=conn.remote_ip,
            src_port=conn.remote_port,
            dest_port=conn.local_port,
            command=f"STOR {filename}",
            raw_bytes=file_bytes,
            full_path=conn.full_path,
            banner=conn.banner,
            notes=[f"CWD: {conn.cwd}", "file uploaded via STOR — content may contain malware, do not execute"]
        )
        
        # schedule background save without blocking main flow
        asyncio.create_task(save_event_background(event_obj))

        await conn.send("226 Transfer complete")