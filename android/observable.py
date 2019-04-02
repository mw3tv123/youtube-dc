observers = []


def register(observer):
    if observer not in observers:
        observers.append(observer)


def unregister(observer):
    if observer in observers:
        observers.remove(observer)


def notify_observers(*args, **kwargs):
    if kwargs["mode"] == "debug":
        for observer in observers:
            observer.debug(*args, **kwargs)

    if kwargs["mode"] == "update":
        for observer in observers:
            observer.download_status(*args, **kwargs)

    if kwargs["mode"] == "warning":
        for observer in observers:
            observer.warning(*args, **kwargs)

    if kwargs["mode"] == "error":
        for observer in observers:
            observer.error(*args, **kwargs)
