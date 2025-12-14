_registry: dict = {} # stores session info for peers

# store session for a peer
def set_session_info(peer: tuple, info: dict) -> None:
    if peer:
        _registry[peer] = info

# pop session for a peer
def pop_session_info(peer: tuple) -> dict | None:
    if not peer:
        return None
    return _registry.pop(peer, None)