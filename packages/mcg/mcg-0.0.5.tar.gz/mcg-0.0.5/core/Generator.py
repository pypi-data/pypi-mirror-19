from abc import ABCMeta, abstractmethod


class Generator(metaclass=ABCMeta):

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def insert_into_file(self):
        pass
