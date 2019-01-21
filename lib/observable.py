observers = []


def register(observer):
    if observer not in observers:
        observers.append(observer)


def unregister(observer):
    if observer in observers:
        observers.remove(observer)


def notify_observers(*args, **kwargs):
    for observer in observers:
        observer.update(*args, **kwargs)
