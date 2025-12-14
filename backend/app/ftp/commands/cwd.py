from app.ftp.connection import FTPConnection
from app.ftp.base_command import BaseCommand

# CWD command
class CwdCommand(BaseCommand):
    async def handle(self, conn: FTPConnection, arg: str):
        if not arg:
            await conn.send("550 Failed to change directory.")
            return

        # Normalize path
        new_path = _normalize_path(conn.cwd, arg)

        # Update it
        conn.cwd = new_path
        await conn.send(f"250 Directory successfully changed.")

# function to normalize ftp paths
def _normalize_path(cwd: str, path: str) -> str:
    # if path starts with '/' start at root
    if path.startswith("/"):
        parts = path.split("/")
    else:
        # otherwise start at current working directory
        parts = (cwd + "/" + path).split("/")

    cleaned = []

    for p in parts:
        if p == "" or p == ".":
            # empty paths do nothing so skip
            continue

        if p == "..":
            # go up one directory but not above root
            if cleaned:
                cleaned.pop()
            # otherwise stay at root
            continue

        # add normal path part
        cleaned.append(p)

    # reconstruct normalized path
    normalized = "/" + "/".join(cleaned)

    return normalized

