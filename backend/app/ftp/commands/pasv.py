import asyncio

from app.ftp.base_command import BaseCommand
from app.ftp.connection import FTPConnection

class PasvCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, arg):
        # close previous data socket if any (TODO: check if necessary)
        if conn.data_sock:
            conn.data_sock.close()
            conn.data_sock = None

        # let OS pick a free port
        server = await asyncio.start_server(
            lambda r, w: setattr(conn, "data_conn", (r, w)),
            host="127.0.0.1",
            port=0
        )
        conn.data_sock = server

        # get actual port
        sock = server.sockets[0]
        port = sock.getsockname()[1]
        p1, p2 = port // 256, port % 256

        # send passive info to client
        await conn.send(f"227 Entering Passive Mode (127,0,0,1,{p1},{p2})")
