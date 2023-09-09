from abc import ABC, abstractmethod


# Observer and Observable classes
class Observer(ABC):
    @abstractmethod
    def update(self, observable, *args, **kwargs):
        pass


class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(self, *args, **kwargs)
