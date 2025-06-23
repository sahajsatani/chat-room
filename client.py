import socket

host = '192.168.88.250'
port = 12345


def client():
    nick = input("NICKNAME: ")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    s.send(nick.encode("ascii"))
    # stdscr.addstr(f"Rooms available are {','.join(self.rooms_name)}")
    while True:
        msg = input(f">")
        s.sendall(msg.encode("ascii"))
        if "exit" in msg:
            break
        # data = s.recv(1024)
        # if data:
        #     print(f"Server: {data.decode()}")



if __name__ == "__main__":
    client()