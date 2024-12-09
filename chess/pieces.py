from abc import ABC, abstractmethod
from enum import Enum

from piece_behaviours import DiagonalMove, KnightMove, MoveMechanism, StraigtMove, StraigtOrDiagonalMove

class Color(Enum):
    black = "black"
    white = "white"

class PieceType(Enum):
    King = "king"
    Queen = "queen"
    Rook = "rook"
    Bishop = "bishop"
    Knight = "knight"
    Pawn = "pawn"

class Position:
    def __init__(self, r, c):
        self.set_position(r, c)

    def get_position(self):
        return (self.__r, self.__c)
    
    def set_position(self, r, c):
        self.__r = r
        self.__c = c

class Piece(ABC):
    __position : Position
    __color : Color
    __move_mechanism : MoveMechanism
    __max_steps : int
    __piece_type : PieceType

    @property
    def piece_type(self):
        return self.__piece_type.value
    
    @property
    def color(self):
        return self.__color.value

    def __init__(self, r:int, c:int, color:Color, move_mechanism: MoveMechanism, piece_type:PieceType, max_steps:int=None):
        self.__position = Position(r, c)
        self.__color = color # TODO
        self.__move_mechanism = move_mechanism
        self.__max_steps = max_steps
        self.__piece_type = piece_type

    def is_valid(self, new_r, new_c):
        return self.__move_mechanism.is_valid(*self.__position.get_position(), new_r, new_c)

    def move_iterator(self, new_r, new_c):
        if not self.is_valid(new_r, new_c):
            raise Exception("Invalid Move for the piece")
        return self.__move_mechanism.move_iterator(*self.__position.get_position(), new_r, new_c)

    def move(self, new_r, new_c):
        if not self.is_valid(new_r, new_c):
            raise Exception("Invalid Move for the piece")
        self.__position.set_position(new_r, new_c)
    
    def can_kill(self):
        pass

    def __str__(self):
        return f"{self.color[0]} {self.piece_type}"

    
def piece_factory(r:int, c:int, piece_type:PieceType, color:Color):
    piece_to_move_mechanism_mapping = {
        PieceType.King : StraigtOrDiagonalMove,
        PieceType.Queen : StraigtOrDiagonalMove,
        PieceType.Rook : StraigtMove,
        PieceType.Bishop : DiagonalMove,
        PieceType.Knight : KnightMove,
        PieceType.Pawn : StraigtOrDiagonalMove,
    }
    piece_to_max_steps_mapping = {
        PieceType.King : 1,
        PieceType.Pawn : 1,
    }
    return Piece(
        r=r,
        c=c,
        color=color,
        move_mechanism=piece_to_move_mechanism_mapping.get(piece_type),
        piece_type=piece_type,
        max_steps=piece_to_max_steps_mapping.get(piece_type)
    )

