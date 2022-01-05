"""UI module"""
import abc

from life import GameOfLife


class UI(abc.ABC):
    """UI class"""

    def __init__(self, life: GameOfLife) -> None:
        self.life = life

    @abc.abstractmethod
    def run(self) -> None:
        """run method"""
        pass
