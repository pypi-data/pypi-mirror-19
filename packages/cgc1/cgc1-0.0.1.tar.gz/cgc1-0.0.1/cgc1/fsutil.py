import datetime
import contextlib
import tempfile
import shutil
import os
import logging

@contextlib.contextmanager
def atomic_open_for_write(filename, mode='w+', **kwargs):
    try:
        with tempfile.NamedTemporaryFile(
                mode=mode, delete=False,
                dir=os.path.dirname(filename), **kwargs) as handle:
            tmpname = handle.name
            yield handle
        os.rename(tmpname, filename)
    finally:
        try:
            if tmpname is not None:
                os.remove(tmpname)
        except (IOError, OSError):
            pass

def format_time(t):
    return "{}-{:06d}".format(t.strftime("%s"), t.microsecond)

def make_backup(filename, backup_pattern="{filename}.{time}.backup~"):
    now = format_time(datetime.datetime.utcnow())
    backup_f = backup_pattern.format(filename=filename, time=now)
    if not os.path.exists(backup_f):
        try:
            shutil.copyfile(filename, backup_f)
        except: # still a race condition
            if os.path.exists(filename):
                raise

def atomic_open_for_write_with_backup(
        filename, mode='w+'):
    make_backup(filename)
    logging.debug("opening for write with backup {!r}".format(filename))
    return atomic_open_for_write(filename, mode)
