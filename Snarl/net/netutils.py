def send(conn, msg):
    """Encode the given message and send it over the given connection.
    """
    conn.sendall(msg.encode())

def receive(conn):
    """Receive and decode a message from the given connection.
    """
    packet = conn.recv(4096)
    msg = packet.decode('utf-8')
    return msg