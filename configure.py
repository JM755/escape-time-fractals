from abc import ABCMeta, abstractmethod

class Configuration(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def with_kwargs(cls, **attrs):
        for arg in attrs:
            if hasattr(cls, arg):
                setattr(cls, arg, attrs[arg])
            else:
                print(f"Attribute: \'{arg}\' does not exist in this class, and has been ignored.")