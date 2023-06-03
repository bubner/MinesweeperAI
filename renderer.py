# Lucas Bubner, 2023

import pygame

from sys import exit
from game import Minesweeper
from ai import AI


def main():
    # Define height and width of the grid we need to render
    BOARD_HEIGHT = 16
    BOARD_WIDTH = 16

    # Define colour scheme to use in program, using RGB format
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)

    # Create game window with pygame, using information from the display to get dimensions
    pygame.init()
    display_info = pygame.display.Info()
    size = width, height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    # Import and initialise new object for the minesweeper game
    # Set mine count to floor(width * height / 6) to get a decent difficulty
    # e.g. 16x16 board = 256 cells, 256 // 6 = 42 mines
    game = Minesweeper(BOARD_WIDTH, BOARD_HEIGHT,
                       BOARD_WIDTH * BOARD_HEIGHT // 6)
    ai = AI(BOARD_HEIGHT, BOARD_WIDTH)

    # Font configuration
    OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
    font = pygame.font.Font(OPEN_SANS, 20)
    heading = pygame.font.Font(OPEN_SANS, 36)

    # Compute board size by calculating first 66% of the board size horizontally,
    # then adding proper padding on each dimension. This lets us calculate the size of each cell
    # programmatically, so if we want a bigger board we can simply change BOARD_WIDTH and BOARD_HEIGHT
    BOARD_PADDING = 20
    board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
    board_height = height - (BOARD_PADDING * 2)
    # Pick the smaller cell size to scale properly on either the X or Y axis
    cell_size = int(min(board_width / BOARD_WIDTH,
                    board_height / BOARD_HEIGHT))
    # 0,0 origin point relative to the board, by offsetting by the padding
    board_origin = (BOARD_PADDING, BOARD_PADDING)

    # Add images for mines and flags, scale them to the proportion of the newly calculated cell sizes
    flag = pygame.image.load("assets/images/flag.png")
    flag = pygame.transform.scale(flag, (cell_size, cell_size))
    mine = pygame.image.load("assets/images/mine.png")
    mine = pygame.transform.scale(mine, (cell_size, cell_size))

    while True:
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
                pygame.draw.rect(screen, GREY, rect)
                # Render a black seperating border around the grey squares
                pygame.draw.rect(screen, BLACK, rect, 3)

                # Add flags to the board if they are flagged
                if game.is_flagged((i, j)):
                    screen.blit(flag, rect)
                # If we've lost the game (by clicking a mine), render all mines
                elif game.is_lost() and game.is_mine((i, j)):
                    screen.blit(mine, rect)
                # Otherwise, if the square is visible, render the number of mines around it
                elif game.is_visible((i, j)):
                    neighbours = game.nearby_mines((i, j))
                    # Render the number of mines around the square
                    text = font.render(str(neighbours), True, WHITE)
                    text_rect = text.get_rect()
                    text_rect.center = rect.center
                    screen.blit(text, text_rect)

                row.append(rect)
            # Append these rows to a 2d array for use in locating certain squares
            # This will be in the format of a 2d representation of the board in the cells[] array
            # e.g.
            # [[rect, rect, rect, rect],
            # [rect, rect, rect, rect],
            # [rect, rect, rect, rect],
            # [rect, rect, rect, rect]]
            cells.append(row)

        # Reset button, calculate dimensions using the padding and height parameters we've used before
        resetButton = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING, (1 / 2) * height - 20,
            (width / 3) - BOARD_PADDING * 2, 50
        )
        buttonText = font.render("Reset", True, WHITE)
        buttonRect = buttonText.get_rect()
        buttonRect.center = resetButton.center
        pygame.draw.rect(screen, GREY, resetButton)
        screen.blit(buttonText, buttonRect)

        # Play best move button, will play the best move available to the AI
        bestMoveButton = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING, (1 / 2) * height - 80,
            (width / 3) - BOARD_PADDING * 2, 50
        )
        buttonText = font.render("Play Best Move", True, WHITE)
        buttonRect = buttonText.get_rect()
        buttonRect.center = bestMoveButton.center
        pygame.draw.rect(screen, GREY, bestMoveButton)
        screen.blit(buttonText, buttonRect)

        # Render text to the screen if the game is won or lost
        text = "You lose!" if game.is_lost() else "You win!" if game.is_won() else ""
        text = heading.render(text, True, WHITE)
        textRect = text.get_rect()
        # Calculate the center of the screen, then offset it to get the center of the right side of the screen
        textRect.center = (int((5 / 6) * width), int((5 / 6) * height))
        screen.blit(text, textRect)

        # Render number of flags that should be placed
        text = "Flags: {}".format(game.minecount - len(game.flags))
        text = font.render(text, True, WHITE)
        textRect = text.get_rect()
        textRect.center = (int((5 / 6) * width), int((2 / 3) * height))
        screen.blit(text, textRect)

        # Render a header text to the screen
        text = heading.render("MINESWEEPER", True, WHITE)
        textRect = text.get_rect()
        textRect.center = (int((5 / 6) * width), int((1 / 6) * height))
        screen.blit(text, textRect)

        # Pygame global event loop, handles user input
        for event in pygame.event.get():
            # If the user presses the X button, exit the program
            if event.type == pygame.QUIT:
                exit()
            # Check if the user is pressing a mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                # Left mouse button
                if event.button == 1:
                    # Check if the user is clicking the reset button
                    if resetButton.collidepoint(mouse_position):
                        game.reset()
                    elif bestMoveButton.collidepoint(mouse_position):
                        # Make an AI move if we press Best Move button
                        move = ai.make_safe_move()
                        if not move:
                            move = ai.make_random_move()
                            if move:
                                print("AI has played a random move.")
                            else:
                                print("No moves are left.")
                    else:
                        # Otherwise, check if the user is clicking a cell
                        for i in range(BOARD_WIDTH):
                            for j in range(BOARD_HEIGHT):
                                # Make a move if the user is clicking a cell
                                if cells[i][j].collidepoint(mouse_position):
                                    game.make_move((i, j))
                                    # Update AI knowledge base
                                    ai.add_knowledge(
                                        (i, j), game.nearby_mines((i, j)))
                # Right mouse button
                elif event.button == 3:
                    # Check if the user is clicking a cell
                    for i in range(BOARD_WIDTH):
                        for j in range(BOARD_HEIGHT):
                            # Change the flag if the user is clicking a cell
                            if cells[i][j].collidepoint(mouse_position):
                                game.change_flag((i, j))

        pygame.display.update()


if __name__ == "__main__":
    main()
