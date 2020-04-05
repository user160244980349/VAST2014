from abc import ABCMeta, abstractmethod


class IReader:

    __metaclass__ = ABCMeta

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(IReader, cls).__new__(cls)
        return cls.instance

    @abstractmethod
    def open(self, path):
        """Read line from file"""
        pass

    @abstractmethod
    def read(self):
        """Read line from file"""
        pass

    @abstractmethod
    def close(self):
        """Read line from file"""
        pass
