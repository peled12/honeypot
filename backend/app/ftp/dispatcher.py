import asyncio
from app.ftp.commands import COMMANDS
from app.ftp.db_utild import save_event_background
from app.schemas import EventCreate
from app.ftp.commands.no_op import NoOpCommand
from app.ftp.rate_limit import check_ftp_rate_limit
from .connection import FTPConnection

# handles dispatching commands to the correct handler
async def dispatch_command(command: str, arg: str, conn: FTPConnection):
    """
    Dispatch the command to the correct handler.
    If unknown command, runs NoOpCommand.
    """

    # check rate limit
    if not check_ftp_rate_limit(conn.remote_ip):
        await conn.send("421 Too many requests")

    # stor command is handled separately
    if command != "STOR":
        event_obj = await EventCreate.from_ftp(
            src_ip=conn.remote_ip,
            src_port=conn.remote_port,
            dest_port=conn.local_port,
            command=f"{command} {arg or ''}",
            raw_bytes=None,
            full_path=conn.full_path,
            banner=conn.banner,
            notes=[f"CWD: {conn.cwd}"]
        )
        
        # save event in backgroud withount blocking main flow
        asyncio.create_task(save_event_background(event_obj))

    # get the command handler
    handler = COMMANDS.get(command, NoOpCommand())
    await handler.handle(conn, arg) # call the handler
