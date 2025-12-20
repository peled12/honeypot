import asyncio
import uuid
from app.utils.banner_rotation import get_ftp_banner

class FTPConnection:
    def __init__(self, reader: "asyncio.StreamReader", writer: "asyncio.StreamWriter"):
        self.reader = reader
        self.writer = writer

        sock = writer.get_extra_info("sockname")
        addr = writer.get_extra_info("peername")
        self.remote_ip = addr[0]
        self.remote_port = addr[1]
        self.local_port = sock[1]

        self.username = None
        self.logged_in = False

        # for uploads
        self.data_sock = None
        self.data_conn = None

        self.session_id = str(uuid.uuid4())
        self.full_path = f"ftp://{self.remote_ip}:{self.local_port}/session/{self.session_id}"
        self.banner = get_ftp_banner(self.remote_ip)
        self.cwd = "/"

    # send
    async def send(self, message: str):
        self.writer.write(f"{message}\r\n".encode('utf-8'))
        await self.writer.drain()

    # receive
    async def receive(self) -> str:
        try:
            data = await self.reader.readline()
            if not data:
                return ""
            return data.decode("utf-8").strip()
        except ConnectionResetError:
            return ""

    # close
    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

    # read data socket (for uploads)
    async def read_data_socket(self):
        if not self.data_sock:
            return b""

        reader, writer = await self.data_conn  # set by pasv command
        chunks = []
        while True:
            data = await reader.read(4096)
            if not data:
                break
            chunks.append(data)

        writer.close()
        await writer.wait_closed()

        # close the server socket
        self.data_sock.close()
        self.data_sock = None
        self.data_conn = None

        return b"".join(chunks)

