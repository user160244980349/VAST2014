from abc import ABCMeta, abstractmethod


class IParser:

    __metaclass__ = ABCMeta

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(IParser, cls).__new__(cls)
        return cls.instance

    @abstractmethod
    def parse_line(self):
        """Parse content line"""
        pass
