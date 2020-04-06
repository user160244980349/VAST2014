import os
import re


def ext(path):
    return re.match(r'^.*\.(.*)$', os.path.basename(path)).group(1)


def name(path):
    return re.match(r'^(.*)\..*$', os.path.basename(path)).group(1)


def fullname(path):
    return os.path.basename(path)


def normalized_name(path):
    return re.sub('[ !@#$.,]', '', name(path)).lower()


def directory(path):
    return os.path.dirname(path)


def files(path):
    fs = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        fs.extend([os.path.join(os.path.abspath(dirpath), filename) for filename in filenames])
    return fs
