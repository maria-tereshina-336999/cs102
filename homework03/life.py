import pathlib
import random
import typing as tp
from random import randint
from copy import copy, deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
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
        # Copy from previous assignment
        grid = []
        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                if randomize == True:
                    znach = random.randint(0, 1)
                else:
                    znach = 0
                grid[i].append(znach)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        x1 = cell[0]
        y1 = cell[1]

        mas = []
        for i in range(x1 - 1, x1 + 2):
            for j in range(y1 - 1, y1 + 2):
                if 0 <= i <= self.rows - 1 and 0 <= j <= self.cols - 1:
                    if x1 != i or y1 != j:
                        mas.append(self.curr_generation[i][j])

        return mas

        pass

    def get_next_generation(self) -> Grid:
        grid_copy = deepcopy(self.curr_generation)
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[0])):
                k=(i,j)
                l=sum(self.get_neighbours(k))
                if l!=2 and l!=3 and self.curr_generation[i][j]==1:
                    grid_copy[i][j]=0
                elif l==3 and self.curr_generation[i][j]==0:
                    grid_copy[i][j]=1
        return grid_copy
        pass

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation=deepcopy(self.curr_generation)
        self.curr_generation=self.get_next_generation()
        self.generations=self.generations+1



        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations<=self.max_generations
        pass

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation!=self.curr_generation
        pass

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """

        with open(filename, "r") as file:
            mas1 = [i.split() for i in file]
            mas2 = [list(str(mas1[i][0])) for i in range(len(mas1))]
            mas3 = [[int(j) for j in mas2[i]] for i in range(len(mas2))]
            return (mas3)
        pass

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, "w")
        l = ["".join(map(str, self.curr_generation[i])) for i in range(len(self.curr_generation))]
        k = "\n".join(l)
        file.write(str(k))
        file.close()
        pass
