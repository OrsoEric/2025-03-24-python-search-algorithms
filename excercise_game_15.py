"""
Solve Game 15 at various board sizes

Algorithm

state



"""
import logging
import random
import pygame  # Import pygame for graphical rendering

import random

class Grid:
    def __init__(self, i_n_size: int = 2):
        c_n_void = 0
        # Size of the grid
        self.n_size = i_n_size
        # Grid configuration (initially ordered)
        self.lln_board = [[r * i_n_size + c + 1 for c in range(i_n_size)] for r in range(i_n_size)]
        # Designate the last cell as void (empty space) by convention
        self.lln_board[-1][-1] = c_n_void

    def __repr__(self):
        # Return a string representation of the grid
        board_str = "\n".join(["\t".join(map(str, row)) for row in self.lln_board])
        return f"Grid({self.n_size}x{self.n_size}):\n{board_str}"
    
    def shuffle(self):
        # Flatten the grid into a list
        flat_board = [tile for row in self.lln_board for tile in row]
        # Shuffle the list randomly
        random.shuffle(flat_board)
        # Map the shuffled list back into the grid
        self.lln_board = [flat_board[i:i+self.n_size] for i in range(0, len(flat_board), self.n_size)]

    def save(self):
        # Return the current grid as a list of lists (for saving)
        return [row[:] for row in self.lln_board]

    def load(self, saved_state):
        # Load the grid from a saved state (list of lists)
        if len(saved_state) != self.n_size or any(len(row) != self.n_size for row in saved_state):
            raise ValueError("Invalid saved state: does not match grid size")
        self.lln_board = [row[:] for row in saved_state]


class Board(Grid):
    def __init__(self, i_n_size: int = 2):
        # Initialize the parent class (Grid)
        super().__init__(i_n_size)
    
    def start_window(self):
        # Initialize pygame
        pygame.init()
        # Set up the display
        self.screen = pygame.display.set_mode((400, 400))  # Window size (width x height)
        pygame.display.set_caption('Game 15')  # Title of the window
        self.font = pygame.font.Font(None, 40)  # Font for rendering tile numbers
        self.running = True  # To control the game loop

    def update(self):
        # Clear the screen
        self.screen.fill((255, 255, 255))  # White background

        # Constants for spacing and tile size
        margin = 3
        tile_size = (400 - margin * (self.n_size + 1)) // self.n_size

        # Draw the tiles
        for r in range(self.n_size):
            for c in range(self.n_size):
                value = self.lln_board[r][c]
                if value != 0:  # Skip the void tile
                    # Position with spacing applied
                    x = c * (tile_size + margin) + margin
                    y = r * (tile_size + margin) + margin

                    # Draw a rectangle for the tile
                    pygame.draw.rect(
                        self.screen, (0, 0, 255),  # Blue color
                        (x, y, tile_size, tile_size)  # Position and size with margin
                    )
                    # Render the tile number
                    text = self.font.render(str(value), True, (255, 255, 255))  # White text
                    text_rect = text.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
                    self.screen.blit(text, text_rect)  # Draw the text on the screen

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        filename="debug.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    
    logging.info("Begin")

    # Create a Board instance
    board = Board(4)  # You can specify different grid sizes here

    backup = board.save()

    # Initialize the pygame window
    board.start_window()

    # Log the initial board configuration
    logging.info(f"Initial Board:\n{repr(board)}")

    # Shuffle the board
    board.shuffle()

    # Log the shuffled board configuration
    logging.info(f"Shuffled Board:\n{repr(board)}")

    board.load( backup )
    logging.info(f"Restore:\n{repr(board)}")

    # Game loop
    while board.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit when the window is closed
                board.running = False
        
        # Update the game state visually
        board.update()

    # Quit pygame
    pygame.quit()
    logging.info("End")
