from abc import ABC, abstractmethod


class Schema(ABC):
    """
    An abstract class containing fields and functions needed for the creation of more specific schema classes

    ...

    Attributes
    ----------
    :DB_NAME : str
        the name of the database file
    :DB_PATH : str
        the path to the database file

    Methods
    -------
    :insert(self) -> (str, dict):
        Returns a tuple containing the insertion string and the values dictionary
    """

    DB_PATH = './data/database.db'
    LIMIT = 10

    @abstractmethod
    def insert(self) -> (str, dict):
        pass

    @staticmethod
    @abstractmethod
    def create() -> str:
        pass

    @staticmethod
    @abstractmethod
    def select_row_with_id(_id: int) -> str:
        pass
