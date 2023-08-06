import logging
from itertools import chain

def log_call(logging_function, function, name, *args, **kwargs):
    if name is None:
        name = function.__name__
    args_s = ", ".join(chain(
        map(repr, args), ("{}={}".format(k, v) for k, v in kwargs.items())))
    logging_function("{}({})".format(name, args_s))
    return function(*args, **kwargs)

