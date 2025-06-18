from abc import ABCMeta, abstractmethod


class BaseSmsGateway(metaclass=ABCMeta):

    @abstractmethod
    def call(self, provider, method, **kwargs):
        ...