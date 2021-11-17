"""This script generates a Sudoku puzzle; solves it and checks the solution"""
import pathlib
import random
import typing as tp

TypeVar = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open(encoding="utf-8") as file:
        puzzle = file.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    """Создает поле с Судоку, имеющее красивый вид"""
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[TypeVar], number: int) -> tp.List[tp.List[TypeVar]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    arr = [values[i * number : i * number + number] for i in range(len(values) // number)]
    return arr


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [grid[i][pos[1]] for i in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    first_ind = pos[0] // 3 * 3
    second_ind = pos[1] // 3 * 3
    arr = []
    for i in range(3):
        for j in range(3):
            arr.append(grid[first_ind + i][second_ind + j])
    return arr


def find_empty_positions(grid: tp.List[tp.List[str]]):
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for ind_i, val_i in enumerate(grid):
        for ind_j, val in enumerate(val_i):
            if val == ".":
                return (ind_i, ind_j)
    return None  # no empty positions found


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    possible_values = set(str(i) for i in range(1, 10))  # initially all digits
    block = get_block(grid, pos)
    column = get_col(grid, pos)
    row = get_row(grid, pos)
    possible_values.difference_update(block)
    possible_values.difference_update(column)
    possible_values.difference_update(row)
    return possible_values


def solve(grid: tp.List[tp.List[str]]):
    """Решение Судоку"""
    solver(grid)
    return grid


def solver(grid: tp.List[tp.List[str]]) -> bool:
    """Recursive function. Simple backtracking"""
    position = find_empty_positions(grid)
    if position is None:
        return True  # the puzzle is completed
    possible_values = find_possible_values(grid, position)
    for value in possible_values:
        grid[position[0]][position[1]] = value
        if solver(grid):
            return True
        grid[position[0]][position[1]] = "."
    return False


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    if isinstance(solution, bool):
        return False  # solution type is bool if puzzle cannot be resolved
    for ind_i, val_i in enumerate(solution):
        for ind_j, val in enumerate(val_i):
            if val == ".":
                return False  # solution is not full
            position = (ind_i, ind_j)
            tested_block = get_block(solution, position)
            tested_row = get_row(solution, position)
            tested_column = get_col(solution, position)
            if (
                len(tested_block) != len(set(tested_block))
                or len(tested_column) != len(set(tested_column))
                or len(tested_row) != len(set(tested_row))
            ):
                return False
    return True


def generate_sudoku(number_of_elements: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = []
    for _ in range(9):
        temp_row = []
        for _ in range(9):
            temp_row.append(".")
        grid.append(temp_row)
    grid = solve(grid)
    if number_of_elements < 81:
        k = 81 - number_of_elements
    else:
        k = 0
    for _ in range(k):
        first_ind = random.randint(0, 8)
        second_ind = random.randint(0, 8)
        while grid[first_ind][second_ind] == ".":
            first_ind = random.randint(0, 8)
            second_ind = random.randint(0, 8)
        grid[first_ind][second_ind] = "."
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        puzzle_grid = read_sudoku(fname)
        display(puzzle_grid)
        puzzle_solution = solve(puzzle_grid)
        if not puzzle_solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(puzzle_solution)
