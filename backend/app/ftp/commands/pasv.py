import asyncio
import os
import random

from app.ftp.base_command import BaseCommand
from app.ftp.connection import FTPConnection

# TODO: fix bug storing files: "421 Service not available, remote server has closed connection." check the error message in the ftp docker container logs

PASV_PORTS = list(range(50000, 50011))
PUBLIC_FTP_IP = os.getenv("PUBLIC_FTP_IP", "127.0.0.1")

class PasvCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, arg):
        # pick a free port from the range
        for _ in range(len(PASV_PORTS)):
            port = random.choice(PASV_PORTS)
            
            try:
                server = await asyncio.start_server(
                    lambda r, w: setattr(conn, "data_conn", (r, w)),
                    host="0.0.0.0",
                    port=port,
                )
                break
            except OSError:
                continue
        else:
            await conn.send("421 No free ports available for PASV")
            return
        
        conn.data_sock = server

        # get actual port
        sock = server.sockets[0]
        port = sock.getsockname()[1]

        # calculate the socket's host parts and port parts
        h1, h2, h3, h4 = PUBLIC_FTP_IP.split(".")
        p1, p2 = port // 256, port % 256

        # send passive info to client
        await conn.send(f"227 Entering Passive Mode ({h1},{h2},{h3},{h4},{p1},{p2})")
