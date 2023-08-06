"""Untilities for using gdo with python build scripts."""

import contextlib
import subprocess
import sys


def target():
    return sys.argv[3]

oldopen = open


def if_changed(targets):
    subprocess.call(['gdo','--if','Changed']+targets)
    if code != 0:
        exit(1)


def if_created(targets):
    subprocess.call(['gdo','--if','Created']+targets)
    if code != 0:
        exit(1)


@contextlib.contextmanager
def open(path, *args, **kwargs):
    if_changed([path])
    try:
        f = oldopen(path, *args, **kwargs)
        yield f
    finally:
        f.close()


def readfile(path, *args, **kwargs):
    with open(path, *args, **kwargs) as f:
        return f.read()
