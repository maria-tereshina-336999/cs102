"генерация и решение лабиринта"
from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    "генерация заготовки для поля"
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param coord:
    :return:
    """
    cols = len(grid[0])
    x, y = coord[0], coord[1]
    direction = choice(("up", "right"))
    # проверим, не сносим ли мы внешнюю стенку лабиринта
    if x == 1 and y == cols - 2:
        direction = "no possible steps"
    elif x == 1:
        direction = "right"
    elif y == cols - 2:
        direction = "up"
    # непосредственно сносим стенку
    if direction == "right":
        grid[x][y + 1] = " "
    elif direction == "up":
        grid[x - 1][y] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    for cell in empty_cells:
        remove_wall(grid, cell)
    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """
    return [
        (row[0], cell[0]) for row in enumerate(grid) for cell in enumerate(row[1]) if cell[1] == "X"
    ]


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param k:
    :return:
    """
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if grid[x][y] == k:
                if x != len(grid) - 1 and grid[x + 1][y] == 0:
                    grid[x + 1][y] = k + 1
                if x != 0 and grid[x - 1][y] == 0:
                    grid[x - 1][y] = k + 1
                if y != len(grid[0]) - 1 and grid[x][y + 1] == 0:
                    grid[x][y + 1] = k + 1
                if y != 0 and grid[x][y - 1] == 0:
                    grid[x][y - 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    :param grid:
    :param exit_coord:
    :return:
    """
    path = [exit_coord]
    x, y = exit_coord[0], exit_coord[1]
    k = int(grid[x][y])
    while k != 1:
        if x != len(grid) - 1 and grid[x + 1][y] == k - 1:
            x += 1
            path.append((x, y))
        if x != 0 and grid[x - 1][y] == k - 1:
            x -= 1
            path.append((x, y))
        if y != len(grid[0]) - 1 and grid[x][y + 1] == k - 1:
            y += 1
            path.append((x, y))
        if y != 0 and grid[x][y - 1] == k - 1:
            y -= 1
            path.append((x, y))
        k -= 1
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid:
    :param coord:
    :return:
    """
    x, y = coord[0], coord[1]
    if x == 0:
        if grid[x + 1][y] == "■":
            return True
    elif x == len(grid) - 1:
        if grid[x - 1][y] == "■":
            return True
    elif y == 0:
        if grid[x][y + 1] == "■":
            return True
    elif y == len(grid[0]) - 1:
        if grid[x][y - 1] == "■":
            return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    :param grid:
    :return:
    """
    # вход и выход совпадают
    exits = get_exits(grid)
    if len(exits) == 1:
        return grid, [exits[0]]
    # вход или выход в тупике
    if encircled_exit(grid, exits[0]) or encircled_exit(grid, exits[1]):
        return grid, None
    grid_before_solving = deepcopy(grid)
    exit_1, exit_2 = exits
    grid[exit_1[0]][exit_1[1]], grid[exit_2[0]][exit_2[1]] = 1, 0
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if grid[x][y] == " ":
                grid[x][y] = 0
    k = 1
    while grid[exit_2[0]][exit_2[1]] == 0:
        grid = make_step(grid, k)
        k += 1
    path = shortest_path(grid, exit_2)
    return grid_before_solving, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
