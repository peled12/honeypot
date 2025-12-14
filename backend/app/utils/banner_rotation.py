import random

from app.redis_client import redis_client

#  profiles and banners

HTTP_BANNERS = [
    "Apache/2.4.52 (Ubuntu)",
    "Apache/2.4.41 (Ubuntu)",
    "nginx/1.18.0 (Ubuntu)",
    "nginx/1.22.1",
    "LiteSpeed",
    "Caddy",
    "Microsoft-IIS/10.0",
]

SSH_PROFILES = {
    "ubuntu_20_04": {
        "id": "ubuntu_20_04",
        "banner": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3",
        "motd": "Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.15.0-124-generic x86_64)",
        "uname": "Linux {host} 5.15.0-124-generic #124-Ubuntu SMP x86_64 GNU/Linux",
        "prompt": "{user}@{host}:~$ ",
    },
    "debian_11": {
        "id": "debian_11",
        "banner": "SSH-2.0-OpenSSH_8.4p1 Debian-5+deb11u1",
        "motd": "Debian GNU/Linux 11 (bullseye)",
        "uname": "Linux {host} 5.10.0-18-amd64 #1 SMP x86_64 GNU/Linux",
        "prompt": "{user}@{host}:~$ ",
    },
    "centos_7": {
        "id": "centos_7",
        "banner": "SSH-2.0-OpenSSH_7.4p1",
        "motd": "CentOS Linux 7 (Core)",
        "uname": "Linux {host} 3.10.0-1160.el7.x86_64 #1 SMP x86_64 GNU/Linux",
        "prompt": "{user}@{host}:~# ",
    },
}

SSH_KEYS = list(SSH_PROFILES.keys())

FTP_BANNERS = [
    "ProFTPD 1.3.6 Server",
    "(vsFTPd 3.0.5)",
    "Pure-FTPd server ready",
    "Microsoft FTP Service",
    "FileZilla Server 0.9.60 beta",
    "wu-ftpd 2.6.2 ready",
]

# rotaion logic

def _next_index(redis_key: str, list_length: int):
    """
    Get next index from Redis. If missing, create a random starting index.
    """
    value = redis_client.get(redis_key)

    if value is None:
        # random starting index
        index = random.randint(0, list_length - 1)
        redis_client.set(redis_key, index)
        return index

    # next index
    index = (int(value) + 1) % list_length
    redis_client.set(redis_key, index)
    return index


def get_http_banner(ip: str) -> str:
    """Return the next HTTP banner for a given IP."""
    redis_key = f"rotation:http:{ip}"
    index = _next_index(redis_key, len(HTTP_BANNERS))
    return HTTP_BANNERS[index]


def get_ssh_profile(ip: str) -> dict:
    """Return the next sequential SSH profile for a given IP."""
    redis_key = f"rotation:ssh:{ip}"
    index = _next_index(redis_key, len(SSH_KEYS))
    key = SSH_KEYS[index]
    return SSH_PROFILES[key]

def get_ftp_banner(ip: str) -> str:
    """Return the next FTP banner for a given IP."""
    redis_key = f"rotation:ftp:{ip}"
    index = _next_index(redis_key, len(FTP_BANNERS))
    return FTP_BANNERS[index]
