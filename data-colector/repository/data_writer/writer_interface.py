import abc


class WriterInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def write(summoner_data: dict):
        pass
