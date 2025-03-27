"""
Solve Game 15 at various board sizes

Algorithm

state



"""

import logging
import random
import pygame


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

    def compute_distance(self, saved_state):
        # Validate the saved state
        if len(saved_state) != self.n_size or any(len(row) != self.n_size for row in saved_state):
            raise ValueError("Invalid saved state: does not match grid size")

        # Create a new grid to hold Manhattan distances
        distance_grid = [[0 for _ in range(self.n_size)] for _ in range(self.n_size)]

        # Compute the Manhattan distance for each tile
        for r in range(self.n_size):
            for c in range(self.n_size):
                value = self.lln_board[r][c]
                if value == 0:
                    continue  # Skip the void tile
                # Find the correct position of the current value in the saved state
                for target_r in range(self.n_size):
                    for target_c in range(self.n_size):
                        if saved_state[target_r][target_c] == value:
                            # Calculate the Manhattan distance
                            distance = abs(r - target_r) + abs(c - target_c)
                            distance_grid[r][c] = distance
                            break

        return distance_grid


class Board(Grid):
    def __init__(self, i_n_size: int = 2):
        # Initialize the parent class (Grid)
        super().__init__(i_n_size)
        self.lln_starting_configuration = self.save()

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

        #compute distance of tiles to starting grid
        lln_distance = self.compute_distance( self.lln_starting_configuration )

        #Compute max distance
        n_max_distance = max(max(lln_distance))
        # Draw the tiles
        for r in range(self.n_size):
            for c in range(self.n_size):
                value = self.lln_board[r][c]
                if value != 0:  # Skip the void tile
                    # Position with spacing applied
                    x = c * (tile_size + margin) + margin
                    y = r * (tile_size + margin) + margin

                    # Determine the color based on Manhattan distance
                    n_distance = lln_distance[r][c]
                    if n_distance == 0:  # Correct position
                        color = (0, 0, 255)  # Blue
                    elif n_max_distance <= 1:
                        color = (0, 255, 0)  # Green
                    else:
                        n_green = 255 * (n_max_distance-n_distance)/(n_max_distance-1)
                        color = (255-n_green, n_green, 0)  # Green

                    # Draw a rectangle for the tile
                    pygame.draw.rect(
                        self.screen, color,
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

    # Compute Manhattan distance to the saved state
    distance_grid = board.compute_distance(backup)
    print("Manhattan Distance Grid:")
    for row in distance_grid:
        print(row)

    if (False):
        board.load( backup )
        logging.info(f"Restore Backup:\n{repr(board)}")

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
