# Lucas Bubner, 2023
from random import shuffle


class Statement:
    """
    A logical statement about a condition in a Minesweeper game.
    Statements are used to represent boolean expressions about knowledge in a game,
    and contain information about a gamestate based on statement parameters.
    """

    def __init__(self, cells, count):
        # Every statement holds a copy of the game state,
        # for internal knowledge representation
        self.cells = set(cells)
        # Every statement also has a count of the number of bombs in the internal set
        self.count = count

    def __eq__(self, other):
        """
        Allow comparison between statements by overriding __eq__
        """
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        """
        Support stringification of statements
        """
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If the number of cells are bomb counts are the same, then these cells are bombs
        return self.cells if self.count == len(self.cells) else None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If there are no bombs in the set, then all the cells are safe
        return self.cells if self.count == 0 else None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Mark a cell as a mine by decrementing the bomb count and removing the cell from the cells set
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Mark a cell as a safe cell by removing the cell from the cells set
        # However, do not change the bomb counter as we know it is safe
        if cell in self.cells:
            self.cells.remove(cell)


class AI:
    """
    AI implementation to play best moves for Minesweeper based on a knowledge base
    """

    def __init__(self, height, width):
        # Set height and width of the board
        self.height = height
        self.width = width

        # Store all statements as 'knowledge', which is an array of statements
        # containing boolean expressions about a games state based on the provided
        # statement parameters. These parameters can base from anything vague to
        # specific details depending on how this knowledge was added.
        self.knowledge = []

        # Interally store squares clicked, discovered to be safe, or marked as a mine
        # by the knowledge base. Player clicked flags are not represented to be marked as mines.
        self.moves = set()
        self.mines = set()
        self.safes = set()

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge statements
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge statements
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new statement to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new statenents to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board, based on the knowledge base.
        """
        # Find a cell in safes that hasn't been picked before
        cells = self.safes.difference(self.moves)
        # Return the first cell in the set, or null if there are no safe cells
        return cells.pop() if len(cells) > 0 else None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Keep track of cells that we can pick from
        pickable_cells = []

        # Loop over the board and add cells that are not mines and have not been picked
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves and cell not in self.mines:
                    pickable_cells.append(cell)

        # Return a random cell from the pickable cells, or null if there are no pickable cells
        shuffle(pickable_cells)
        return pickable_cells[0] if len(pickable_cells) > 0 else None
