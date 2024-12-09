

from abc import ABC, abstractmethod


def i_iterator(old_i, new_i):
    if old_i==new_i: # if old_i == new_i, we need to return the same number even if row is not changing but column is
        yield old_i
    for r in range(old_i+1, new_i): # if old_i<new_i
        yield r
    for r in range(old_i-1, new_i, -1): # if old_i>new_i
        yield r

class MoveMechanism(ABC):
    @staticmethod
    @abstractmethod
    def is_valid(old_r, old_c, new_r, new_c):
        pass

    @classmethod
    @abstractmethod
    def move_iterator(cls, old_r, old_c, new_r, new_c):
        pass

class DiagonalMove(MoveMechanism):
    @staticmethod
    def is_valid(old_r, old_c, new_r, new_c):
        return (abs(old_r-new_r) == abs(old_c-new_c))
    
    @classmethod
    def move_iterator(cls, old_r, old_c, new_r, new_c):
        if not cls.is_valid(old_r, old_c, new_r, new_c):
            raise Exception("Invalid Move for the piece")
        for r in i_iterator(old_r, new_r):
            for c in i_iterator(old_c, new_c):
                if abs(old_r-r)==abs(old_c-c):
                    yield r, c

class StraigtMove(MoveMechanism):
    @staticmethod
    def is_valid(old_r, old_c, new_r, new_c):
        return (old_r-new_r == 0 or  old_c-new_c==0)
    
    @classmethod
    def move_iterator(cls, old_r, old_c, new_r, new_c):
        if not cls.is_valid(old_r, old_c, new_r, new_c):
            raise Exception("Invalid Move for the piece")
        for r in i_iterator(old_r, new_r):
            for c in i_iterator(old_c, new_c):
                yield r, c

class StraigtOrDiagonalMove(MoveMechanism):
    @staticmethod
    def is_valid(*args, **kwargs):
        return StraigtMove.is_valid(*args, **kwargs) or DiagonalMove.is_valid(*args, **kwargs)
    
    @classmethod
    def move_iterator(cls, *args, **kwargs):
        if StraigtMove.is_valid(*args, **kwargs):
            return StraigtMove.move_iterator(*args, **kwargs) # try if it's a straigt move
        if DiagonalMove.is_valid(*args, **kwargs):
            return DiagonalMove.move_iterator(*args, **kwargs) # if it's a diagonal move

class KnightMove(MoveMechanism):
    @staticmethod
    def is_valid(old_r, old_c, new_r, new_c):
        row_diff = abs(old_r-new_r)
        col_diff = abs(old_c-new_c)
        return (row_diff==2 and col_diff==1) or (row_diff==1 and col_diff==2)

    @classmethod
    def move_iterator(cls, old_r, old_c, new_r, new_c):
        pass # Knight can jump over other pieces so we can skip this.