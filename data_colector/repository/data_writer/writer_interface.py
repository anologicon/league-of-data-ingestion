import abc
from typing import List


class WriterInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def write(self, file_path: str, json_data: [List, dict]):
        pass
