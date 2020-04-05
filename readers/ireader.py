from abc import ABCMeta, abstractmethod


class IReader:
    __metaclass__ = ABCMeta

    @abstractmethod
    def read_line(self):
        """Переместить объект"""
        pass
