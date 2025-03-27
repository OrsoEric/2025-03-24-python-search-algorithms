"""
Solve Game 15 at various board sizes

Algorithm

state



"""

import logging
import random
import pygame
from typing import List, Tuple

class Cl_grid:
    def __init__(self, i_n_size: int = 2):
        self.c_n_void = 0
        # Size of the grid
        self.n_size = i_n_size
        # Grid configuration (initially ordered)
        self.lln_board = [[r * i_n_size + c + 1 for c in range(i_n_size)] for r in range(i_n_size)]
        # Designate the last cell as void (empty space) by convention
        self.lln_board[-1][-1] = self.c_n_void

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

    def load(self, i_lln_saved_state : List[List[int]] ):
        # Load the grid from a saved state (list of lists)
        if len(i_lln_saved_state) != self.n_size or any(len(row) != self.n_size for row in i_lln_saved_state):
            raise ValueError("Invalid saved state: does not match grid size")
        self.lln_board = [row[:] for row in i_lln_saved_state]

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

    @staticmethod
    def log(i_lln_saved_state: List[List[int]]):
        """
        Log the given saved state into the logger.
        """
        logging.info("Saved State:")
        for row in i_lln_saved_state:
            logging.info("\t" + "\t".join(map(str, row)))

class Cl_board(Cl_grid):
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
        #THIS IS BUGGED it takes the max of first element. maximum unfathomable
        #n_max_distance = max(max(lln_distance))
        n_max_distance = 0
        for r in range(self.n_size):
            for c in range(self.n_size):
                n_value = lln_distance[r][c]
                if n_value > n_max_distance:
                    n_max_distance = n_value

        # Draw the tiles
        for r in range(self.n_size):
            for c in range(self.n_size):
                n_value = self.lln_board[r][c]
                if n_value != 0:  # Skip the void tile
                    # Position with spacing applied
                    x = c * (tile_size + margin) + margin
                    y = r * (tile_size + margin) + margin

                    ln_color = (0, 0, 0)  # BLACK
                    # Determine the color based on Manhattan distance
                    n_distance = lln_distance[r][c]
                    if n_distance > n_max_distance:
                        print(f"ERR: Max {n_max_distance} | dist: {n_distance}")
                        ln_color = (0, 0, 0)  # BLACK
                    elif n_distance == 0:  # Correct position
                        ln_color = (0, 0, 255)  # Blue
                    elif n_max_distance <= 1:
                        ln_color = (0, 255, 0)  # Green
                    else:
                        n_green = 255 * (n_max_distance-n_distance)/(n_max_distance-1)

                        if n_green < 0:
                            print(f"ERR: {n_green} | Max {n_max_distance} | dist: {n_distance}")
                            n_green = 0
                            
                        elif n_green > 255:
                            print(f"ERR: {n_green} | Max {n_max_distance} | dist: {n_distance}")
                            n_green = 255

                        ln_color = (255-n_green, n_green, 0)  # Green

                    # Draw a rectangle for the tile
                    pygame.draw.rect(
                        self.screen,
                        ln_color,
                        (x, y, tile_size, tile_size)  # Position and size with margin
                    )
                    # Render the tile number
                    text = self.font.render(str(n_value), True, (255, 255, 255))  # White text
                    text_rect = text.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
                    self.screen.blit(text, text_rect)  # Draw the text on the screen

        # Update the display
        pygame.display.flip()

class Solver:
    def __init__(self, i_cl_board : Cl_board):
        self.cl_board : Cl_board = i_cl_board
        #save solved configuration
        self.lln_solved : List[List[int]] = i_cl_board.save()

        return    
        
    def list_actions(self, i_lln_saved_state: List[List[int]]):
        """
        From a given state, list all possible actions for the void.
        Actions involve swapping the void with its neighboring tiles.
        Actions are represented as tuples: (row_void, col_void, row_target, col_target).
        """
        n_size = len(i_lln_saved_state)
        void_position = None

        # Locate the void position (value 0)
        for r in range(n_size):
            for c in range(n_size):
                if i_lln_saved_state[r][c] == 0:
                    void_position = (r, c)
                    break
            if void_position:
                break

        if not void_position:
            raise ValueError("No void (0) found in the given state.")

        n_void_h, n_void_w = void_position
        ltn_actions = []

        # List all possible moves by checking bounds
        if n_void_h > 0:  # Move up
            ltn_actions.append((n_void_w, n_void_h, n_void_w, n_void_h - 1))
        if n_void_h < n_size - 1:  # Move down
            ltn_actions.append((n_void_w, n_void_h, n_void_w, n_void_h + 1))
        if n_void_w > 0:  # Move left
            ltn_actions.append((n_void_w, n_void_h, n_void_w - 1, n_void_h))
        if n_void_w < n_size - 1:  # Move right
            ltn_actions.append((n_void_w, n_void_h, n_void_w + 1, n_void_h))

        return ltn_actions
    
    def evaluate_score(self, i_lln_saved_state: List[List[int]]) -> int:
        """
        Given a state, evaluate its score
        I take the total sum of every distance
        When the board is solved, score is zero
        """

        #logging.info("Reference board:")
        #Cl_grid.log( self.lln_solved )

        lln_distance = self.cl_board.compute_distance( i_lln_saved_state )
        logging.info("evaluate_score distance:")
        Cl_grid.log(lln_distance)
        n_score = 0
        for ln_distance in lln_distance:
            for n_distance in ln_distance:
                n_score += n_distance

        #SUM is bugged too... I expected sum of sum fould sum an array...
        #n_score = sum(sum(lln_distance))
        return n_score

    def execute_action( self, i_lln_state : List[List[int]], i_tn_action : Tuple[int] ) -> bool:
        """
        from a given state, execute an action
        """

        #unpack action
        (n_void_w, n_void_h, n_item_w, n_item_h) = i_tn_action

        n_void = i_lln_state[n_void_h][n_void_w]
        if n_void != cl_board.c_n_void:
            logging.error(f"ERR: position {i_tn_action} is not a VOID {n_void} ")
            return True #FAIL

        n_item = i_lln_state[n_item_h][n_item_w]
        if n_item == cl_board.c_n_void:
            logging.error(f"ERR: position {i_tn_action} is not an ITEM {n_item} ")
            return True #FAIL       

        #perform the swap
        i_lln_state[n_void_h][n_void_w] = n_item
        i_lln_state[n_item_h][n_item_w] = n_void

        return False #OK


    def solve(self):

        n_score = self.evaluate_score( self.lln_solved )
        logging.info(f"Score Solved: {n_score}")

        lln_shuffled = self.cl_board.save()
        n_score = self.evaluate_score( lnn_shuffled)
        logging.info(f"Score Shuffled: {n_score}")

        # List all possible actions from the saved state
        ltn_actions = self.list_actions(lnn_shuffled)
        logging.info(f"Actions: {ltn_actions}")
        
        tn_action = ltn_actions[0]
        self.execute_action(lnn_shuffled,tn_action)
        logging.info(f"Execute Action: {tn_action}")
        Cl_grid.log(lnn_shuffled)

        #for tn_action in ltn_actions:
            

        

        
        return


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
    cl_board = Cl_board(5)  # You can specify different grid sizes here

    # Initialize the Solver
    cl_solver = Solver( cl_board )

    lln_solved_state = cl_board.save()

    # Initialize the pygame window
    cl_board.start_window()

    # Log the initial board configuration
    logging.info(f"Initial Board:\n{repr(cl_board)}")

    # Shuffle the board
    cl_board.shuffle()
    lnn_shuffled = cl_board.save()
    # Log the shuffled board configuration
    logging.info(f"Shuffled Board:\n{repr(cl_board)}")

    # Compute Manhattan distance to the saved state
    distance_grid = cl_board.compute_distance(lln_solved_state)
    print("Manhattan Distance Grid:")

    for row in distance_grid:
        print(row)

    if (False):
        cl_board.load( lln_solved_state )
        logging.info(f"Restore Backup:\n{repr(cl_board)}")


    cl_solver.solve()


    # Game loop
    while cl_board.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit when the window is closed
                cl_board.running = False

        # Update the game state visually
        cl_board.update()


    
    





    # Quit pygame
    pygame.quit()
    logging.info("End")
