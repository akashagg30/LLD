
from board import Board
from pieces import Color
from player import Player


class Game:
    __board : Board = None
    __player1 : Player = None
    __player2 : Player = None
    __current_player : Player = None

    @property
    def is_current_player_black(self):
        return self.__current_player==self.__player2

    @property
    def is_current_player_white(self):
        return not self.is_current_player_black

    @property
    def color_of_current_player(self) -> Color:
        return Color.black if self.is_current_player_black else Color.white
    
    def __init__(self, player1:Player, player2:Player):
        self.__board = Board()
        self.__player1 = player1
        self.__player2 = player2
        self.__current_player = player1
    
    def current_player_move(self):
        move_input = input(f"{self.__current_player.name}, your move : ")
        old_r, old_c, new_r, new_c = list(map(int, move_input.split(" ")))
        try:
            self.__board.move(
                old_r=old_r,
                old_c=old_c,
                new_r=new_r,
                new_c=new_c
            )
            self.__current_player = self.__player1 if self.is_current_player_black else self.__player2 # changing current player
        except BaseException as e:
            print(e)
        self.__board.draw()
    
    def play(self):
        self.__board.draw()
        while True:
            self.current_player_move()

if __name__ == "__main__":
    Game(Player("a"), Player("b")).play()