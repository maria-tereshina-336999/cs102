import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i, row in enumerate(self.life.curr_generation):
            for j, cell in enumerate(row):
                symb = "*" if cell == 1 else " "
                screen.addch(i + 1, j + 1, symb)

    def run(self) -> None:
        screen = curses.initscr()
        curses.resize_term(self.life.rows + 2, self.life.cols + 2)
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            life.step()
            curses.napms(100)
        curses.endwin()


if __name__ == "__main__":
    life = GameOfLife((24, 80), max_generations=100)
    ui = Console(life)
    ui.run()
