import time

def send(conn, msg):
    """Encode the given message and send it over the given connection.
    """
    conn.sendall(msg.encode())
    # This solves an intermittent bug with concatenation of server messages.
    # Yes, it's bad, but fine for this application.
    time.sleep(0.0001)

def receive(conn):
    """Receive and decode a message from the given connection.
    """
    packet = conn.recv(4096)
    msg = packet.decode('utf-8')
    return msg