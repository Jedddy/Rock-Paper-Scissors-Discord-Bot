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
        return type(self) == type(other)

        
class Rock(Move):
    def __str__(self):
        return "Rock"
    
    def __lt__(self, other):
        return type(other) == Paper
    
    def __gt__(self, other):
        return type(other) == Scissors
            

class Paper(Move):
    def __str__(self):
        return "Paper"
    
    def __lt__(self, other):
        return type(other) == Scissors
    
    def __gt__(self, other):
        return type(other) == Rock

class Scissors(Move):
    def __str__(self):
        return "Scissors"

    def __lt__(self, other):
        return type(other) == Rock
    
    def __gt__(self, other):
        return type(other) == Paper
         