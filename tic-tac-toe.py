import os
import time

class Game():

    DEFAULT_RAW_COUNTER = 3
    DEFAULT_DRAW_COUNTER = 9

    def __init__(self):
        self.turn = "x"
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


    def update_canvas(self):
        os.system("cls")
        print(f"\tMove {self.config[self.turn]['color']}")
        self.ingame_board_visual = [
            [f"\t{self.ingame_board[1]} | {self.ingame_board[2]} | {self.ingame_board[3]}\t"], self.right_ingame_board_visual[0:10],
            ["\t— + — + —"], self.right_ingame_board_visual[10:21],
            [f"\t{self.ingame_board[4]} | {self.ingame_board[5]} | {self.ingame_board[6]}\t"], self.right_ingame_board_visual[21:31],
            ["\t— + — + —"], self.right_ingame_board_visual[31:42],
            [f"\t{self.ingame_board[7]} | {self.ingame_board[8]} | {self.ingame_board[9]}\t"], self.right_ingame_board_visual[42:55]
        ]
        output = str()
        for board_chunk in self.ingame_board_visual:
            output += "".join(board_chunk)
        print(output)

    def check_for_draw(self):
        for cell in self.ingame_board:
            if self.ingame_board[cell] != " ":
                self.draw_counter -= 1
        if self.draw_counter == 0:
            for plate in self.ingame_board:
                self.ingame_board[plate] = self.config[self.ingame_board[plate]]["color"]
                self.update_canvas()
                time.sleep(0.2)
            self.game = False
        self.draw_counter = Game.DEFAULT_DRAW_COUNTER

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
            self.check_for_draw()
            self.update_canvas()
            if not self.game:
                break
            try:
                p_turn = int(input("\tI'll go on... "))
                if p_turn > 9 or p_turn <= 0:
                    raise ValueError
                if self.ingame_board[p_turn] == " ":
                    self.right_ingame_board_visual = self.right_ingame_board_visual.replace(str(p_turn), " ")
                    self.ingame_board[p_turn] = self.turn
                    self.check_for_win()
                    self.turn = self.config[self.turn]["turn"]
                else: raise ValueError
            except ValueError:
                continue

if __name__ == "__main__":
    Game().start()