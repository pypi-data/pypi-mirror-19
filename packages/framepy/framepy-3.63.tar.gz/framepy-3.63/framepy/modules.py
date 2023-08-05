from abc import ABCMeta, abstractmethod


class Module(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def before_setup(self, properties, arguments, beans):
        raise NotImplementedError()

    @abstractmethod
    def after_setup(self, properties, arguments, context, beans_initializer):
        raise NotImplementedError()
