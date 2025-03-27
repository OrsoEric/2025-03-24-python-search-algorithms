import pygame
import sys
import random

class FifteenBoard:
    def __init__(self, rows ):
        cols = rows
        self.rows = rows
        self.cols = cols
        self.board = [[r * cols + c + 1 for c in range(cols)] for r in range(rows)]
        self.board[-1][-1] = 0  # Empty space
        self.empty = (rows - 1, cols - 1)
        self.shuffle()

    def shuffle(self):
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for _ in range(1000):
            r, c = self.empty
            move = random.choice(moves)
            new_r, new_c = r + move[0], c + move[1]
            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                self.board[r][c], self.board[new_r][new_c] = self.board[new_r][new_c], self.board[r][c]
                self.empty = (new_r, new_c)

    def move_tile(self, r, c):
        er, ec = self.empty
        if abs(er - r) + abs(ec - c) == 1:
            self.board[er][ec], self.board[r][c] = self.board[r][c], self.board[er][ec]
            self.empty = (r, c)

    def draw(self, screen, tile_size):
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.board[r][c]
                rect = pygame.Rect(c * tile_size, r * tile_size, tile_size, tile_size)
                if value != 0:
                    pygame.draw.rect(screen, (200, 200, 200), rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(value), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(screen, (50, 50, 50), rect)

def main(rows):
    cols = rows
    pygame.init()
    tile_size = 100
    screen = pygame.display.set_mode((cols * tile_size, rows * tile_size))
    pygame.display.set_caption("Fifteen Board")
    clock = pygame.time.Clock()
    board = FifteenBoard(rows)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                r, c = y // tile_size, x // tile_size
                board.move_tile(r, c)

        screen.fill((255, 255, 255))
        board.draw(screen, tile_size)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main(5)  # Change parameters for different board sizes (e.g., 3x3, 5x5)
