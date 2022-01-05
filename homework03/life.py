"""GameOfLife module"""
import pathlib
import random
import typing as tp
from copy import deepcopy

# import pygame
# from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    """class for GameOfLife"""

    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """creates grid for game"""
        if randomize:
            return [[random.randint(0, 1) for j in range(self.cols)] for i in range(self.rows)]
        return [[0 for j in range(self.cols)] for i in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        """returns list of neighbours for given cell"""
        x, y = cell[0], cell[1]
        neighbours = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i <= self.rows - 1 and 0 <= j <= self.cols - 1:
                    if x != i or y != j:
                        neighbours.append(self.curr_generation[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        """returns next generation for game"""
        grid_copy = deepcopy(self.curr_generation)
        for i, row in enumerate(self.curr_generation):
            for j, val in enumerate(row):
                k = (i, j)
                numb_of_neighbours = sum(self.get_neighbours(k))
                if numb_of_neighbours != 2 and numb_of_neighbours != 3 and val == 1:
                    grid_copy[i][j] = 0
                elif numb_of_neighbours == 3 and val == 0:
                    grid_copy[i][j] = 1
        return grid_copy

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded and self.is_changing:
            self.prev_generation = deepcopy(self.curr_generation)
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            return self.generations >= self.max_generations
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, encoding="utf-8") as file:
            grid = [[int(j) for j in i.strip()] for i in file]
        life_game = GameOfLife((len(grid), len(grid[0])))
        life_game.curr_generation = grid
        return life_game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as file:
            for i in self.curr_generation:
                print(*i, sep="", file=file)
