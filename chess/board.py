
from typing import List, Optional

from pieces import Color, Piece, PieceType, piece_factory


class Board:
    # Black pieces at top, white at bottom
    __board : List[List[Piece]]
    __killed_pieces = []

    
    def __init__(self):
        self.__set_initial_board()

    def get_piece_at_position(self, r, c) -> Piece:
        if not (0<=r<8 and 0<=c<8):
            raise Exception("Invalid Position entered")
        return self.__board[r][c]
    
    def move(self, old_r, old_c, new_r, new_c):
        if not (0<=new_r<8 and 0<=new_c<8):
            raise Exception("Invalid Position entered")
        piece = self.get_piece_at_position(old_r, old_c)
        if not piece:
            raise Exception(f"Invalid Move, no piece at [{old_r}{old_c}]")
        if self.does_any_piece_lies_in_path(old_r, old_c, new_r, new_c):
            raise Exception("Invalid Move, you can't jump over pieces")
        piece.is_valid(new_r, new_c)

        if self.__board[new_r][new_c]:
            self.__killed_pieces.append(self.__board[new_r][new_c])
        
        self.__board[new_r][new_c] = piece
        self.__board[old_r][old_c] = None

        piece.move(new_r, new_c)

    def does_any_piece_lies_in_path(self, old_r, old_c, new_r, new_c):
        piece : Piece = self.get_piece_at_position(old_r, old_c)
        if piece.piece_type == "pawn":
            return (
                old_c==new_c # straight move by rook
                and self.get_piece_at_position(new_r, new_c) # and a piece exists in front of rook
            )
        elif piece.piece_type == "knight" or (abs(old_r-new_r)<2 and abs(old_c-new_c)<2):
            return False
        else:
            for r, c in piece.move_iterator(new_r,new_c):
                if self.__board[r][c]:
                    return True
            return False


    def __set_initial_board(self):

        self.__board = [[None for i in range(8)] for i in range(8)]
        # setting pawns
        for c in range(8):
            self.__board[1][c] = piece_factory(1, c, PieceType.Pawn, Color.black)
            self.__board[6][c] = piece_factory(6, c, PieceType.Pawn, Color.white)
        # setting rooks
        self.__board[0][0] = piece_factory(0, 0, PieceType.Rook, Color.black)
        self.__board[0][7] = piece_factory(0, 7, PieceType.Rook, Color.black)
        self.__board[7][0] = piece_factory(7, 0, PieceType.Rook, Color.white)
        self.__board[7][7] = piece_factory(7, 7, PieceType.Rook, Color.white)
        # setting knights
        self.__board[0][1] = piece_factory(0, 1, PieceType.Knight, Color.black)
        self.__board[0][6] = piece_factory(0, 6, PieceType.Knight, Color.black)
        self.__board[7][1] = piece_factory(7, 1, PieceType.Knight, Color.white)
        self.__board[7][6] = piece_factory(7, 6, PieceType.Knight, Color.white)
        # setting bishops
        self.__board[0][2] = piece_factory(0, 2, PieceType.Bishop, Color.black)
        self.__board[0][5] = piece_factory(0, 5, PieceType.Bishop, Color.black)
        self.__board[7][2] = piece_factory(7, 2, PieceType.Bishop, Color.white)
        self.__board[7][5] = piece_factory(7, 5, PieceType.Bishop, Color.white)
        # setting kings
        self.__board[0][3] = piece_factory(0, 3, PieceType.King, Color.black)
        self.__board[7][3] = piece_factory(0, 3, PieceType.King, Color.white)
        # setting queens
        self.__board[0][4] = piece_factory(0, 4, PieceType.Queen, Color.black)
        self.__board[7][4] = piece_factory(0, 4, PieceType.Queen, Color.white)


    def draw(self):
        print("_"*140)
        for r in range(8):
            if r==0:
                print("  | ", end="")
                for c in range(8):
                    print(f"{c}{' '*7}", end=" | ")
                print()
            print(r, end=" | ")
            for c in range(8):
                elem = (str(self.__board[r][c] if self.__board[r][c] else "-") + " "*10)[:8]
                print(elem, end=" | ")
            print()