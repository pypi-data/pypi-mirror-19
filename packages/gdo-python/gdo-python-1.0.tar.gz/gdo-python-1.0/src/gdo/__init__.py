"""Untilities for using gdo with python build scripts."""

import contextlib
import subprocess


@contextlib.contextmanager
def open(path, *args, **kwargs):
    subprocess.call(['gdo','--if','Changed',path])
    f = open(path, *args, **kwargs)
    yield f
    f.close()
