# Format of cache: {"<packet>": <timestamp>}

limiter = {

}

def add_to_limiter(packet: str, timestamp: float):
    global limiter

    # Check if the packet is already in the cache and timestamp difference is less than 5 seconds
    if packet in limiter:
        time_difference = timestamp - limiter[packet]
        print(f"Time difference: {time_difference}")
        if time_difference < 30:
            return False

    limiter[packet] = timestamp

    return True

