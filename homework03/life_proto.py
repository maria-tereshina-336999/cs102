import random
import typing as tp
from copy import copy, deepcopy
import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:

    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        self.grid=self.create_grid(True)
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.grid=self.get_next_generation()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for i in range(self.cell_height):
            grid.append([])
            for j in range(self.cell_width):
                if randomize == True:
                    znach = random.randint(0, 1)
                else:
                    znach = 0
                grid[i].append(znach)
        return grid
        pass


    def draw_grid(self) -> None:

        x=0
        y=self.cell_size*(-1)
        grid=self.grid
        for i in range(self.cell_height):
            y=y+self.cell_size
            x=0
            for j in range(self.cell_width):
                if grid[i][j]==1:
                    pygame.draw.rect(self.screen, pygame.Color('green'),(x,y,self.cell_size,self.cell_size)  )
                    x=x+self.cell_size
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),(x,y,self.cell_size,self.cell_size ) )
                    x=x+self.cell_size



        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        x1=cell[0]
        y1=cell[1]

        mas=[]
        for i in range(x1-1,x1+2):
            for j in range(y1 - 1, y1 + 2):
                if 0<=i<=self.cell_height-1 and 0<=j<=self.cell_width-1 :
                    if x1!=i or y1!=j:
                        mas.append(self.grid[i][j])

        return mas
        pass

    def get_next_generation(self) -> Grid:
        grid_copy = deepcopy(self.grid)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                k=(i,j)
                l=sum(self.get_neighbours(k))
                if l!=2 and l!=3 and self.grid[i][j]==1:
                    grid_copy[i][j]=0
                elif l==3 and self.grid[i][j]==0:
                    grid_copy[i][j]=1
        return grid_copy

        pass


f=GameOfLife(320,280,20)
f.run()