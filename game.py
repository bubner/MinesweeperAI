# Lucas Bubner, 2023
from random import randrange
from enum import Enum


class Gamestates(Enum):
    """
    Enum to hold current game state
    """
    PLAYING = 0
    WON = 1
    LOST = 2


class Minesweeper:
    """
    Minesweeper implementation
    """
    def __init__(self, width, height, mines):
        # Store width, height, and mine count of the board
        self.width = width
        self.height = height
        self.minecount = mines
        # Store location of all flags
        self.flags = []
        # Store location of all mines, randomly assign them to places
        self.mines = []
        # Store location of all revealed cells
        self.revealed = []
        # Set initial game state to playing
        self.gamestate = Gamestates.PLAYING
        # Generate mines
        self.generate_mines()

    def generate_mines(self):
        """
        Generate mines by randomly selecting a square and checking if it is already a mine, if it is, then we will try again.
        """
        mines_generated = 0
        while mines_generated < self.minecount:
            # Generate a random square
            square = (randrange(self.height), randrange(self.width))
            # If the square is already a mine, try again and do not increment the mines generated
            if square in self.mines:
                continue
            # Otherwise, add it to the mines array and increment successful mines
            self.mines.append(square)
            mines_generated += 1

    def reset(self):
        """
        Reset all variables to default values in the constructor
        """
        self.flags = []
        self.mines = []
        self.revealed = []
        self.gamestate = Gamestates.PLAYING
        self.generate_mines()

    def make_move(self, square):
        """
        Make a move on the board, revealing the square and checking if the game is won or lost
        """
        # Do not click on a flagged square or if the game is won or lost
        if square in self.flags or self.gamestate != Gamestates.PLAYING:
            return
        
        # Add the square to the revealed array
        self.revealed.append(square)

        # If it is the first move, reveal a starting radius of squares around the square
        if len(self.revealed) == 1:
            # Explore neighbours that are not mines
            for neighbour in self.get_neighbours(square):
                if neighbour not in self.mines:
                    self.revealed.append(neighbour)
                
                
        # Check if the revealed square is in the mines locations, if so, then the game is lost
        if square in self.mines:
            self.gamestate = Gamestates.LOST
        

    def change_flag(self, square):
        """
        Flag a square on the board and prevent it from being clicked, or unflag it if it is already flagged
        """
        # Do not flag a square if the game is won or lost
        if self.gamestate != Gamestates.PLAYING:
            return
        # Toggle the presence of a square in the flags array by checking if it is already in the array
        # or if it is already revealed
        if square in self.flags:
            self.flags.remove(square)
        elif square not in self.revealed:
            # Otherwise, add it. This will make sure we have a toggle function
            self.flags.append(square)

        # Check if the game is won by checking if the number of correct flags is equal to the number of mines
        if self.mines == self.flags:
            self.gamestate = Gamestates.WON

    def is_lost(self):
        """
        Determine if the game is lost if the gamestate is set to LOST
        """
        return self.gamestate == Gamestates.LOST
    
    def is_won(self):
        """
        Determine if the game is won if the gamestate is set to WON
        """
        return self.gamestate == Gamestates.WON

    def is_flagged(self, square):
        """
        Determine if a square is flagged by checking if it exists in the flags array
        """
        return square in self.flags

    def is_mine(self, square):
        """
        Determine if a square is a mine by checking if it is in the mines array
        """
        return square in self.mines

    def is_visible(self, square):
        """
        Determine if a square has been revealed by checking if it is in the revealed array
        """
        return square in self.revealed

    def nearby_mines(self, square):
        """
        Determine the number of mines around a square
        """
        # Count the number of mines around a square by checking if the square is in the mines array
        # We can get the neighbours using the get_neighbours function then loop over all those neighbours
        # and check if they are in the mines array to determine nearby mine count
        count = 0
        for neighbour in self.get_neighbours(square):
            if neighbour in self.mines:
                count += 1
        return count

    def get_neighbours(self, square):
        """
        Get the squares that are adjacent to a square
        """
        # Get all neighbours of a square by iterating over a 3x3 grid
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Do not count the target square itself
                if i == 0 and j == 0:
                    continue
                # Append the neighbour to the neighbours array
                neighbours.append((square[0] + i, square[1] + j))
        return neighbours
