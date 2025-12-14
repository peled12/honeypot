import os
import asyncio
from app.ftp.server import FTPServer

def main():
    host = os.getenv("FTP_HOST", "0.0.0.0")
    port = int(os.getenv("FTP_PORT", 2121))

    server = FTPServer(host, port) # get server instance

    # run the async server
    asyncio.run(server.start())

if __name__ == "__main__":
    main()
