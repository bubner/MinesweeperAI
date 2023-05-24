import pygame
import sys

from game import Minesweeper

# Define height and width of the grid we need to render
BOARD_HEIGHT = 16
BOARD_WIDTH = 16

# Define colour scheme to use in program, using RGB format
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Create game window with pygame, using information from the display to get dimensions
pygame.init()
display_info = pygame.display.Info()
size = width, height = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

# Import and initialise new object for the minesweeper game
game = Minesweeper()

# Font configuration
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
font = pygame.font.Font(OPEN_SANS, 20)

# Compute board size by calculating first 66% of the board size horizontally,
# then adding proper padding on each dimension. This lets us calculate the size of each cell
# programmatically, so if we want a bigger board we can simply change BOARD_WIDTH and BOARD_HEIGHT
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
# Pick the smaller cell size to scale properly on either the X or Y axis
cell_size = int(min(board_width / BOARD_WIDTH, board_height / BOARD_HEIGHT))
# 0,0 origin point relative to the board, by offsetting by the padding
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images for mines and flags, scale them to the proportion of the newly calculated cell sizes
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

while True:
    # Pygame global event loop, exit if we need to terminate the app
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Update screen object on resize
    display_info = pygame.display.Info()
    size = width, height = display_info.current_w, display_info.current_h

    # Fill the screen with complete black
    screen.fill(BLACK)

    # Draw board by rendering each rectangle from the board origin
    cells = []
    for i in range(BOARD_HEIGHT):
        row = []
        for j in range(BOARD_WIDTH):
            # Draw rectangle for cell, where the position will be represented by
            # board_origin(axis) + current board axis * the size of the cell, with dimensions of a normal cell_size
            # rect is in the form (left, top, width, height), so we can loop over each position in the height/width matrix
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )

            # Render inner squares grey
            pygame.draw.rect(screen, GRAY, rect)
            # Render a white border around the grey squares
            pygame.draw.rect(screen, WHITE, rect, 1)
            row.append(rect)
        # Append these rows to a 2d array for use in locating certain squares
        # This will be in the format of a 2d representation of the board in the cells[] array
        # e.g.
        # [[0, 0, 0, 0],
        # [0, 0, 0, 0],
        # [0, 0, 0, 0],
        # [0, 0, 0, 0]]
        cells.append(row)

    # Reset button, calculate dimensions using the padding and height parameters we've used before
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = font.render("Reset", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(buttonText, buttonRect)

    # User interaction, check for any mouse input
    left, _, right = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    
    # Check if the user has clicked on the display
    if left == 1 or right == 1:
        if resetButton.collidepoint(mouse_position) and left == 1:
            # Reset the game back to default on a left click of the reset button
            game.reset()
            continue
            
        # Loop over board to check if the player has clicked a square
        for i in range(BOARD_WIDTH):
            for j in range(BOARD_HEIGHT):
                if cells[i][j].collidepoint(mouse_position):
                    # Make a move if it is a left click, or flag if it is a right click
                    game.make_move(cells[i][j]) if left == 1 else game.flag(cells[i][j])

    pygame.display.flip()
