import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size=cell_size
        self.speed=speed
        self.screen_size = (self.life.rows * self.cell_size,  self.life.cols * self.cell_size )
        self.screen = pygame.display.set_mode(self.screen_size)


    def draw_lines(self) -> None:
        for x in range(0, self.screen_size[1], self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.screen_size[0]))
        for y in range(0, self.screen_size[0], self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.screen_size[1], y))
        pass

    def draw_grid(self) -> None:
        x=0
        y=self.cell_size*(-1)
        grid=self.life.curr_generation
        for i in range(self.life.rows):
            y=y+self.cell_size
            x=0
            for j in range(self.life.cols):
                if grid[i][j]==1:
                    pygame.draw.rect(self.screen, pygame.Color('green'),(x,y,self.cell_size,self.cell_size)  )
                    x=x+self.cell_size
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),(x,y,self.cell_size,self.cell_size ) )
                    x=x+self.cell_size



        pass

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
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key==pygame.K_SPACE:
                        while True:
                            event = pygame.event.wait()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    break
                            if event.type==pygame.MOUSEBUTTONDOWN:
                                if event.button==1:
                                    x=event.pos[0]//self.cell_size
                                    y=event.pos[1]//self.cell_size
                                    self.life.curr_generation[y][x]=1
                                    self.draw_grid()
                                    self.draw_lines()
                                    pygame.display.flip()
            self.life.step()
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


        pass


life = GameOfLife((30, 30))
ui = GUI(life)
ui.run()