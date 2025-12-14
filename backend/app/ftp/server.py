import asyncio
import socket
import threading

from app.ftp.connection import FTPConnection
from app.ftp.dispatcher import dispatch_command
from app.ftp.parser import parse_command

class FTPServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def start(self):
        # start the ascync ftp server
        server = await asyncio.start_server(
            self.handle_client,
            host=self.host,
            port=self.port
        )

        # serve forever and close automatically when stops
        async with server:
            await server.serve_forever()
    
    # handle each client connection
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        conn = FTPConnection(reader, writer)

        await conn.send(f"220 {conn.banner}")

        # save the connection
        await dispatch_command("OPTS", "", conn)

        # listen for commands
        try:
            while True:
                raw = await conn.receive()
                if not raw:
                    break

                command, arg = parse_command(raw)

                # dispatch command
                await dispatch_command(command, arg, conn)

        except ConnectionResetError:
            print(f"[FTP] Connection lost from {conn.remote_ip}")
        finally:
            writer.close()
            await writer.wait_closed()