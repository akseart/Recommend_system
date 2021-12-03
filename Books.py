from abc import ABC, abstractmethod
import pandas as pd
import pickle


class AbstractMedia(ABC):
    @abstractmethod
    def get_part(self, page, per_page):
        """
        Args:
            page: Номер страницы
            per_page: Количество страниц для разбиения

        Returns:
            Часть элементов для их отображения на нескольких страницах
        """
        ...

    @abstractmethod
    def get_recommend(self, idx):
        """
        Получение списка рекомендаций
        Args:
            idx: id объекта

        Returns:
            Список рекомендаций
        """
        ...


class AbstractTrainset(ABC):
    @abstractmethod
    def to_inner_iid(self, idx):
        """
        Получение внутреннего(в модели) ключа элемента
        Args:
            idx: внешний ключ элемента

        Returns:
            внутренний(модельный) ключ
        """
        pass

    @abstractmethod
    def to_raw_iid(self, inner_id):
        """
        Получение внешнего ключа
        Args:
            inner_id: внутренний(модельный) ключ

        Returns:
            внешний ключ
        """
        pass


class AbstractModel(ABC):
    trainset: AbstractTrainset = ...

    @abstractmethod
    def get_neighbors(self, inner_id, num) -> list:
        """
        Получение списка "соседей" элемента
        Args:
            inner_id: внутренний(модельный) ключ
            num: количество получаемых элементов

        Returns:
            Список внутренних ключей, рекомендуемых элементов.

        """


class Book(AbstractMedia):
    def __init__(self, book: dict, model: AbstractModel = None):
        self._book = book
        self._list_book = list(self._book.values())
        if model:
            self._model = model

    @classmethod
    def from_csv(cls, path):
        """
        Загрузка используя csv файл.

        Файл должен содержать в себе поля: id, title, genres, authors, year, recommend(список рекомендаций).
        Args:
            path: путь до csv файла
        """
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
                    'recommend': list(map(int, x[1].recomend[1:-1].split(',')))
                }
            for x in book.iterrows()
        }

        return cls(dict_book)

    @classmethod
    def from_model(cls, path_to_model, path_to_csv):
        """
        Загрузка из модели и csv файла.

        Модель должна отвечать требованиям определенным выше.
        CSV файл должен содержать в себе поля: id, title, genres, authors, year.

        Args:
            path_to_model: путь к модели
            path_to_csv: путь к файлу с данными по книгам

        Returns:

        """
        book = pd.read_csv(path_to_csv)
        book.fillna('', inplace=True)

        dict_book = {
            x[1].id:
                {
                    'id': x[1].id,
                    'title': x[1].title,
                    'genres': x[1].genres,
                    'authors': x[1].authors,
                    'year': x[1].year,
                }
            for x in book.iterrows()
        }
        with open(path_to_model, 'rb') as f:
            model = pickle.load(f)

        return cls(dict_book, model)

    def __getitem__(self, item):
        book = self._book[item]
        return book

    def __len__(self):
        return len(self._book)

    def get_part(self, page, per_page):
        return self._list_book[(page - 1) * per_page:(page * per_page)]

    def get_recommend(self, idx):
        """
        Получение списка рекомендаций для определенной книги
        Args:
            idx: id книги

        Returns:
            Список из 7 id, которые являются рекомендации к книги

        """
        if "_model" in self.__dict__:
            inner_id = self._model.trainset.to_inner_iid(idx)

            neighbors_iid = self._model.get_neighbors(inner_id, 7)

            neighbors_id = [self._model.trainset.to_raw_iid(inner_id)
                            for inner_id in neighbors_iid]

            return neighbors_id

        else:
            return self._book[int(idx)]['recommend']
