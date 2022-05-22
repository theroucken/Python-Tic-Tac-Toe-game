import os
import time
import socket
import requests

class Game():

    DEFAULT_RAW_COUNTER = 3
    DEFAULT_DRAW_COUNTER = 9

    def __init__(self):
        self.me = "unknown"
        self.turn = "x"
        self.turn_num = 1
        self.can_move = False
        self.game = True
        self.numbers = tuple([str(num) for num in range(1, 10)])
        self.draw_counter = Game.DEFAULT_DRAW_COUNTER
        self.raw_counter = Game.DEFAULT_RAW_COUNTER
        self.config = {
            "x": {
                "turn": "o",
                "color": "\033[31mx\033[39m"
            },
            "o": {
                "turn": "x",
                "color": "\033[92mo\033[39m"
            },
            "masks": {
                "win": [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
            }
        }

        self.ingame_board = {
            1: " ", 2: " ", 3: " ",
            4: " ", 5: " ", 6: " ",
            7: " ", 8: " ", 9: " "
        }

        self.right_ingame_board_visual = "1 | 2 | 3\n"\
                                        "\t— + — + —\n"\
                                        "4 | 5 | 6\n"\
                                        "\t— + — + —\n"\
                                        "7 | 8 | 9\n"

    def wait_for_players(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 25567))
        self.sock.listen(1)
        print(f"{time.strftime('%X')} Waiting for players")
        self.conn, self.addr = self.sock.accept()
        print(f"{time.strftime('%X')} Player connected: {self.addr}")
        self.me = "host"
        self.start()

    def connect_to_host(self):
        ip = requests.get("https://pastebin.com/raw/XXXXXXXX").text.split(":") # link to address to connect [ip]:[port]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip[0], int(ip[1])))
        self.me = "client"
        print("Connected")
        self.start()


    def update_canvas(self):
        os.system("cls")
        print(f"\tMove {self.config[self.turn]['color']}")
        self.ingame_board_visual = [
            f"\t{self.ingame_board[1]} | {self.ingame_board[2]} | {self.ingame_board[3]}\t", self.right_ingame_board_visual[0:10],
            "\t— + — + —", self.right_ingame_board_visual[10:21],
            f"\t{self.ingame_board[4]} | {self.ingame_board[5]} | {self.ingame_board[6]}\t", self.right_ingame_board_visual[21:31],
            "\t— + — + —", self.right_ingame_board_visual[31:42],
            f"\t{self.ingame_board[7]} | {self.ingame_board[8]} | {self.ingame_board[9]}\t", self.right_ingame_board_visual[42:55]
        ]
        print("".join(board_chunk for board_chunk in self.ingame_board_visual))

    def check_for_win(self):
        for mask in self.config["masks"]["win"]:
            for cell in mask:
                if self.ingame_board[cell] == self.turn:
                    self.raw_counter -= 1
            if self.raw_counter == 0:
                for cell in self.ingame_board:
                    if self.ingame_board[cell] == self.turn:
                        self.ingame_board[cell] = self.config[self.turn]["color"]
                        self.update_canvas()
                        time.sleep(0.7)
                self.game = False
                break
            self.raw_counter = Game.DEFAULT_RAW_COUNTER

    def start(self):
        while True:
            if self.draw_counter == 0:
                for cell in self.ingame_board:
                    self.ingame_board[cell] = self.config[self.ingame_board[cell]]["color"]
                    self.update_canvas()
                    time.sleep(0.3)
                self.game = False
            if not self.game:
                if self.me == "host":
                    self.conn.shutdown(socket.SHUT_RDWR)
                    self.conn.close()
                    self.sock.close()
                else:
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                break
            try:
                if self.me == "host":
                    if self.turn_num % 2 != 0:
                        self.can_move = True
                    else:
                        self.can_move = False
                elif self.me == "client":
                    if self.turn_num % 2 == 0:
                        self.can_move = True
                    else:
                        self.can_move = False
                if self.can_move:
                    self.update_canvas()
                    p_turn = int(input("\tI'll go on... "))
                    if p_turn > 9 or p_turn <= 0:
                        raise ValueError
                    if self.ingame_board[p_turn] == " ":
                        self.right_ingame_board_visual = self.right_ingame_board_visual.replace(str(p_turn), " ")
                        self.ingame_board[p_turn] = self.turn
                        self.check_for_win()
                        self.turn = self.config[self.turn]["turn"]
                        self.draw_counter -= 1
                        if self.me == "host":
                            self.conn.send(str(p_turn).encode())
                        else:
                            self.sock.send(str(p_turn).encode())
                    else: raise ValueError
                else:
                    print("Opponent's move")
                    self.update_canvas()
                    if self.me == "host":
                        p_turn = self.conn.recv(4).decode()
                    else:
                        p_turn = self.sock.recv(4).decode()
                    self.right_ingame_board_visual = self.right_ingame_board_visual.replace(p_turn, " ")
                    self.ingame_board[int(p_turn)] = self.turn
                    self.check_for_win()
                    self.turn = self.config[self.turn]["turn"]
                    self.draw_counter -= 1
                self.turn_num += 1
            except ValueError:
                continue

if __name__ == "__main__":
    if input("1 - host\n2 - client\n> ") == "1":
        Game().wait_for_players()
    else:
        Game().connect_to_host()