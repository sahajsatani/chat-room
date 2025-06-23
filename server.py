import socket
import sys
import threading
import curses
from rich.console import Console
from rich.table import Table
class server:
    host = '127.0.0.1'
    port = 12345
    rooms_member = [[]]
    rooms_name = ["public_room"]
    client = {}
    def __init__(self,host,port):
        self.host = host
        self.port = port
    def handle_user(self,nick, conn, addr, stdscr):
        stdscr.addstr(f"Rooms available are {','.join(self.rooms_name)}\n")
        stdscr.addstr(f"Enter room have to join:\n")
        curses.echo()
        room = stdscr.getstr().decode()
        curses.noecho()
        while room not in self.rooms_name:
            stdscr.addstr(f"{room} not exist\n Choose from {self.rooms_name}\n")
            curses.echo()
            room = stdscr.getstr().decode()
            curses.noecho()


        while True:
            data = conn.recv(1024)
            if not data:
                stdscr.addstr(f"{nick} exiting...\n")
                stdscr.refresh()
                break
            if data:
                # stdscr.clear()
                # stdscr.addstr(f"{nick}: {data.decode()}\n")
                # stdscr.refresh()
                if "quit" in data.decode():
                    # stdscr.clear()
                    stdscr.addstr(f"{nick} exiting...\n")
                    stdscr.refresh()
                    conn.close()
                    break
        conn.close()

    def handle_admin(self, nick, conn, addr, stdscr):
        pass
    def listen(self,stdscr):
        console = Console()
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((self.host,self.port))
        s.listen(4)
        # curses.curs_set(0)

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)

        stdscr.clear()
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr("Welcome to the Chat App\n",curses.color_pair(1))
        stdscr.addstr(f"Server listening on {self.host}:{self.port}\n")
        stdscr.attroff(curses.A_BOLD)
        stdscr.refresh()

        while True:
            conn, addr = s.accept()
            nick = conn.recv(1024).decode()
            if nick == "admin":
                password = conn.recv(1024).decode()
                if password == "pass$123":
                    stdscr.addstr(f"{nick} join to server.\n")
                    stdscr.refresh()
                    threading.Thread(target=self.handle_admin, args=(nick, conn, addr, stdscr)).start()
            else:
                stdscr.addstr(f"{nick} join to server.\n")
                stdscr.refresh()
                t = threading.Thread(target=self.handle_user, args=(nick, conn, addr, stdscr))
                t.start()
        s.close()

if __name__ == "__main__":
    args = sys.argv
    server = server(args[1],args[2])
    curses.wrapper(server.listen)
