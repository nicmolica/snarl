import socket
import subprocess

host = "localhost"
port = 8000

# open a server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # set up the server so it is listening for incoming connections
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()

    # set up a socket to receive data from a connection
    conn, addr = sock.accept()
    with conn:
        # keep recieving data from the connection until receiving the END flag
        data = ""
        while data == "" or "END" not in data[len(data) - 4:]:
            packet = conn.recv(4096)
            data += packet.decode('utf-8')

        # run the a2 program with the input and send the result back to the client
        total = subprocess.run(["./../A2/a2", "--sum"], stdout = subprocess.PIPE, input = data, encoding = 'utf-8')
        conn.sendall(total.stdout.encode())