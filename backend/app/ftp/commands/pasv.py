import asyncio

from app.ftp.base_command import BaseCommand
from app.ftp.connection import FTPConnection

class PasvCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, arg):
        # choose a new port for passive mode
        p1, p2 = 195, 80
        port = p1 * 256 + p2

        # open a data server socket on that port
        data_sock = await asyncio.start_server(
            lambda r, w: setattr(conn, "data_conn", (r, w)),
            host="127.0.0.1",
            port=port
        )
        conn.data_sock = data_sock # keep server reference

        # inform client of passive mode details
        await conn.send(f"227 Entering Passive Mode (127,0,0,1,{p1},{p2})")
