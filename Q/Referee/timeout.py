import threading

class TimeoutError(Exception):
    pass

class InterruptableThread(threading.Thread):
    def __init__(self, func, *args, **kwargs):
        threading.Thread.__init__(self)
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._result = None

    def run(self):
        self._result = self._func(*self._args, **self._kwargs)

    @property
    def result(self):
        return self._result


class InlineTimeout:
    def __init__(self, sec):
        self._sec = sec

    def timeout(self, f, *args, **kwargs):
        it = InterruptableThread(f, *args, **kwargs)
        it.daemon = True
        it.start()
        it.join(self._sec)
        if not it.is_alive():
            return it.result
        raise TimeoutError('execution expired')
