"""Untilities for using gdo with python build scripts."""

import contextlib
import subprocess
import sys


def target():
    return sys.argv[3]

oldopen = open

@contextlib.contextmanager
def open(path, *args, **kwargs):
    code = subprocess.call(['gdo','--if','Changed',path])
    if code != 0:
        exit(1)
    try:
        f = oldopen(path, *args, **kwargs)
        yield f
    finally:
        f.close()


def readfile(path):
    with open(path, mode='r') as f:
        return f.read()
