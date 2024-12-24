# Format of cache: {"<packet>": <timestamp>}

limiter = {

}

def add_to_limiter(packet: str, timestamp: float):
    global limiter

    timestamp_in_seconds = timestamp 
    # Check if the packet is already in the cache and timestamp difference is less than 20 seconds
    if packet in limiter and (timestamp - limiter[packet]) < 20:
        return False

    limiter[packet] = timestamp

    return True

