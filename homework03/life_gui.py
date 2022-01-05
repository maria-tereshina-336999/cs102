import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.height, self.width = (self.life.rows * self.cell_size, self.life.cols * self.cell_size)
        self.screen = pygame.display.set_mode((self.height, self.width))

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, x), (self.height, x))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (y, 0), (y, self.width))

    def draw_grid(self) -> None:
        y = 0
        for row in self.life.curr_generation:
            x = 0
            for cell in row:
                color = pygame.Color("green") if cell else pygame.Color("white")
                pygame.draw.rect(self.screen, color, (y, x, self.cell_size, self.cell_size))
                x += self.cell_size
            y += self.cell_size

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_SPACE:
                        while True:
                            event = pygame.event.wait()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    break
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    x, y = pygame.mouse.get_pos()
                                    prev_cell_state = self.life.curr_generation[
                                        x // self.cell_size
                                    ][y // self.cell_size]
                                    self.life.curr_generation[x // self.cell_size][
                                        y // self.cell_size
                                    ] = (0 if prev_cell_state == 1 else 1)
                                    self.draw_grid()
                                    self.draw_lines()
                                    pygame.display.flip()
            self.life.step()
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((20, 20))
    gui = GUI(life)
    gui.run()
