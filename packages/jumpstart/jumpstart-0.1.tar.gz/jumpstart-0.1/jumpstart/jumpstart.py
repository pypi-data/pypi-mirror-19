from inspect import isgeneratorfunction
from functools import wraps

def now(func):
    @wraps(func)
    def middle(*args, **kwargs):
        def inner():
            gen = func(*args, **kwargs)
            val = yield(next(gen))
            yield None
            yield val
            for each in gen:
                yield each
        inside = inner()
        val = next(inside)
        inside.send(val)
        return inside
    if not isgeneratorfunction(func):
        raise TypeError('Only generator functions can be decorated.')
    return middle
