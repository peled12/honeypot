import asyncio
import uuid
import asyncssh
from app.utils.constants import UNKNOWN
from app.schemas import EventCreate
from app.ssh.db_utild import save_event_sync
from app.ssh.server.registery import pop_session_info

# TODO: figure out why the ssh session is not running

# SSH session class handling user commands
class HoneypotSSHSession(asyncssh.SSHServerSession):
    def __init__(self, *args, **kwargs):
        print("Initializing HoneypotSSHSession")

        # initialize session state
        self._input = ""
        self._chan = None
        self.ip = UNKNOWN
        self.port = None
        self.server_ip = "0.0.0.0"
        self.server_port = 2222
        self.session_id = str(uuid.uuid4())  # fallback if none found
        self.profile = None
        self.attempted_username = None
        self.banner = None
        self.prompt = None
        self.host = None

    def connection_made(self, chan):
        self._chan = chan # set channel
        print("connection made:", chan)

    def connection_lost(self, exc):
        print(f"[ssh.session] channel closed {getattr(self, '_chan', None)}")

    # accept pty requests from the client
    def pty_requested(self, *args, **kwargs):
        print("pty requested", args, kwargs)
        return True

    # allow shell requests from the client
    def shell_requested(self):
        print("shell requested")
        return True

    def session_started(self):
        print("session started")
        # gather peer and sock info
        peer = self._chan.get_extra_info("peername")
        sock = self._chan.get_extra_info("sockname")
        self.ip = peer[0] if peer else UNKNOWN
        self.port = peer[1] if peer else None
        self.server_ip = sock[0] if sock else "0.0.0.0"
        self.server_port = sock[1] if sock else 2222

        # try to get session info created during auth
        peer_key = (self.ip, self.port)
        info = pop_session_info(peer_key)
        if info:
            self.session_id = info.get("session_id", self.session_id)
            self.profile = info.get("profile")
            self.attempted_username = info.get("username")

        # pick a host name: profile name + short session suffix (6 hex chars) for uniqueness
        short = self.session_id.replace("-", "")[:6]
        host = f"{self.profile['id'].split('_')[0]}-{short}"
        self.host = host # assign host
        user = self.attempted_username or "root" # get the username attempted during auth, or default to root

        motd = self.profile["motd"]
        prompt = self.profile["prompt"].format(user=user, host=host)

        # present welcome message and prompt to attacker
        self._chan.write(motd + "\n")
        self._chan.write(prompt)

        # store banner to use in events
        self.banner = self.profile["banner"]
        self.prompt = prompt

    def data_received(self, data, datatype):
        print(f"data received: {data!r}")
        # data: incoming data from client

        self._input += data # accumulate input into buffer

        # process each complete line
        while "\n" in self._input:
            line, _, self._input = self._input.partition("\n")
            
            cmd = line.strip() # get the command

            event_obj = EventCreate.from_ssh(
                src_ip=self.ip,
                src_port=self.port,
                dest_port=self.server_port,
                command=cmd,
                banner=self.banner,
                full_path=f"ssh://{self.server_ip}:{self.server_port}/session/{self.session_id}"
            )

            # save to db and publish to redis
            loop = asyncio.get_running_loop() # get current event loop
            loop.run_in_executor(None, save_event_sync, event_obj) # run the blocking db operation in the background to not block the event loop
            
            if cmd in ("exit", "logout"):
                # simulate logout and exit session
                self._chan.write("logout\n")
                self._chan.exit(0)

             # handle uname command
            elif cmd.startswith("uname"):
                # decide what to output (like uname -a)
                uname_output = self.profile["uname"].format(host=self.host)
                if "-a" in cmd:
                    self._chan.write(uname_output + "\n")
                else:
                    self._chan.write("Linux\n")

            # if its a blank command just redisplay prompt
            elif cmd == "":
                pass

            # other commands
            else:
                self._chan.write(f"bash: {cmd}: command not found\n$ ") # fake command not found
