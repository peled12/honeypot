# get the country based on ip address
import httpx
import ipaddress

from app.utils.constants import COUNTRY_LOCAL


async def get_country_from_ip(ip: str) -> str | None:
  # ignore local or internal IPs (127.0.0.1, etc.)
    if is_private_ip(ip):
        return COUNTRY_LOCAL

    URL = f"https://ipapi.co/{ip}/json/"

    # get the country
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            res = await client.get(URL)
            res.raise_for_status()  # raise error if one occures
            data = res.json()
            return data.get("country_code")
    except Exception as e:
        print(f"Geo lookup failed for {ip}: {e}")
        return None

# checks if an ip is local
def is_private_ip(ip: str) -> bool:
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return False
