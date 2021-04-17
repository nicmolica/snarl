import time

def send(conn, msg):
    print(f"About to send the message: {msg}")
    conn.sendall(msg.encode())
    # TODO Can we just remove this pls? hopefully testing works ok
    #$time.sleep(0.0001) # TODO consider fixing this cause it's pretty bad OR just comment to try to justify it

def receive(conn):
    packet = conn.recv(4096)
    msg = packet.decode('utf-8')
    return msg