import asyncio
import uuid
from app.ssh.rate_limit import check_ssh_rate_limit
from app.utils.constants import UNKNOWN
from app.schemas import EventCreate
from app.ssh.db_utild import save_event_sync
from app.ssh.server.registery import set_session_info
from app.utils.banner_rotation import get_ssh_profile

def password_auth_handler(conn, username: str, password: str) -> bool:
    # client information
    peer = conn.get_extra_info("peername")
    client_ip = peer[0] if peer else UNKNOWN
    client_port = peer[1] if peer else UNKNOWN

    # server information
    sock = conn.get_extra_info("sockname")
    server_ip = sock[0] if sock else "0.0.0.0"
    server_port = sock[1] if sock else 2222

    # rate limiting
    allowed = check_ssh_rate_limit(client_ip)
    if not allowed:
        print(f"[ssh] rate limit exceeded for {client_ip}")
        return False
        
    profile = get_ssh_profile(client_ip) # get profile based on ip rotation
    session_id = str(uuid.uuid4()) # a unique session id to correlate auth + future session events
    
    set_session_info(peer, {"session_id": session_id, "profile": profile, "username": username}) # store this info in registry keyed by peer

    # build event object

    session_id = str(uuid.uuid4()) # unique session id that belongs for this connection
    full_path = f"ssh://{server_ip}:{server_port}/session/{session_id}"

    event_obj = EventCreate.from_ssh(
        src_ip=client_ip,
        src_port=client_port,
        dest_port=server_port,
        command=None,
        banner=profile["banner"],
        full_path=full_path,
        notes=[f"ssh password auth attempt: username={username}, password={password}"]
    )

    loop = asyncio.get_running_loop() # get current event loop
    loop.run_in_executor(None, save_event_sync, event_obj) # run the blocking db operation in the background to not block the event loop

    return True
