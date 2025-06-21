import socket
import threading
import curses
from rich.console import Console
from rich.table import Table
host = '192.168.88.250'
port = 12345

def handle(nick, conn, addr, stdscr):
    while True:
        data = conn.recv(1024)
        if not data:
            # stdscr.clear()
            stdscr.addstr(f"{nick} exiting...\n")
            stdscr.refresh()
            break
        if data:
            # stdscr.clear()
            stdscr.addstr(f"{nick}: {data.decode()}\n")
            stdscr.refresh()
            if "exit" in data.decode():
                # stdscr.clear()
                stdscr.addstr(f"{nick} exiting...\n")
                stdscr.refresh()
                conn.close()
                break
    conn.close()

def listen(stdscr):
    console = Console()
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(4)
    # curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)

    stdscr.clear()
    stdscr.attron(curses.A_BOLD)
    stdscr.addstr("Welcome to the Chat App\n",curses.color_pair(1))

    stdscr.addstr(f"Server listening on host:{host} port:{port}\n")
    stdscr.attroff(curses.A_BOLD)
    stdscr.refresh()

    while True:
        conn, addr = s.accept()
        # stdscr.clear()
        stdscr.addstr(f"Connection with {addr}\n")
        stdscr.refresh()
        nick = conn.recv(1024)
        t = threading.Thread(target=handle, args=(nick.decode(), conn, addr, stdscr))
        t.start()
    s.close()

if __name__ == "__main__":
    curses.wrapper(listen)
