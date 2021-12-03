from abc import ABC, abstractmethod
import pandas as pd


class AbstractMedia(ABC):
    @abstractmethod
    def get_info(self):
        ...


class Book:
    def __init__(self, book: dict):
        self._book = book
        self._list_book = list(self._book.values())

    @classmethod
    def from_csv(cls, path):
        book = pd.read_csv(path)
        book.fillna('', inplace=True)

        dict_book = {
            x[1].id:
                {
                    'id': x[1].id,
                    'title': x[1].title,
                    'genres': x[1].genres,
                    'authors': x[1].authors,
                    'year': x[1].year,
                    'recomend': list(map(int, x[1].recomend[1:-1].split(',')))
                }
                for x in book.iterrows()
        }

        return cls(dict_book)

    def __getitem__(self, item):
        book = self._book[item]
        return book

    def __len__(self):
        return len(self._book)

    def get_list_of_book(self, page, per_page):
        return self._list_book[(page - 1) * per_page:(page * per_page)]
