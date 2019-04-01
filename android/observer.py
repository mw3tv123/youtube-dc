from abc import ABCMeta, abstractmethod


class Observer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def download_status(self, *args, **kwargs):
        pass

    @abstractmethod
    def warning(self, *args, **kwargs):
        pass

    @abstractmethod
    def error(self, *args, **kwargs):
        pass
