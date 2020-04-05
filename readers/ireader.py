from abc import ABCMeta, abstractmethod


class IReader:

    __metaclass__ = ABCMeta

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(IReader, cls).__new__(cls)
        return cls.instance

    @abstractmethod
    def read_line(self):
        """Read line from file"""
        pass
