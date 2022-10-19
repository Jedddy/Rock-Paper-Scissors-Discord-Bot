from abc import ABC, abstractmethod


class Move(ABC):
    """Base Moves Class"""
    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass 

    def __eq__(self, other):
        if type(self) == type(other):
            return True
        return False

        
class Rock(Move):
    def __str__(self):
        return "Rock"
    
    def __lt__(self, other):
        if type(other) == Paper:
            return True
        return False
    
    def __gt__(self, other):
        if type(other) == Scissors:
            return True
        return False


class Paper(Move):
    def __str__(self):
        return "Paper"
    
    def __lt__(self, other):
        if type(other) == Scissors:
            return True
        return False
    
    def __gt__(self, other):
        if type(other) == Rock:
            return True
        return False


class Scissors(Move):
    def __str__(self):
        return "Scissors"

    def __lt__(self, other):
        if type(other) == Rock:
            return True
        return False
    
    def __gt__(self, other):
        if type(other) == Paper:
            return True
        return False