import time
import logging.config
import inspect
import os, os.path
import sys
import logging


def init_logging(filename="logging.ini", defaults=None, base_dir=None):
    """
    init logging system by file
    :param filename:
    :param base_dir:
    :return:
    """
    if base_dir is None:
        base_dir = get_root_dir()
    logging.config.fileConfig(os.path.join(base_dir, filename), defaults=defaults)


def get_root_dir():
    """
    get root file dir of script
    :return:
    """
    cur_frame = inspect.currentframe()
    if cur_frame is None:
        return os.path.abspath(os.getcwd())
    while True:
        root_dir = os.path.dirname(os.path.abspath(cur_frame.f_code.co_filename))
        cur_frame = cur_frame.f_back
        if cur_frame is None:
            break
    return root_dir


def push_cur_dir_into_search_path(idx=0):
    """
    push current path to sys search path
    :param idx: path insert index
    :return:
    """
    sys.path.insert(idx, os.path.abspath(os.getcwd()))


def current_time_in_millis():
    """
    get current time in millis
    :return:
    """
    return int(time.time() * 1000)


cur_ms = current_time_in_millis


def read_line_from_file(filename, mode='r', allow_blank=False, skip_line=0):
    """
    line by line from file
    :param filename: filename
    :param mode: file open mode
    :param allow_blank: whether emit blank line
    :return:
    """
    with open(filename, mode) as fp:
        for line in fp:
            line = line.strip()
            if len(line) == 0 and not allow_blank:
                continue
            if skip_line > 0:
                skip_line -= 1
                continue
            yield line


line_file = read_line_from_file


def asbool(obj):
    """
    convert obj to bool
    :param obj:
    :return:
    """
    if isinstance(obj, basestring):
        obj = obj.strip().lower()
        if obj in ['true', 'yes', 'on', 'y', 't', '1']:
            return True
        elif obj in ['false', 'no', 'off', 'n', 'f', '0']:
            return False
        else:
            raise ValueError("String is not true/false: %r" % obj)
    return bool(obj)


def get_trace():
    import traceback
    return traceback.format_exc()


class Singleton(object):
    _singleton_instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton_instance:
            cls._singleton_instance = super(Singleton, cls).__new__(
                cls, *args, **kwargs)
        return cls._singleton_instance

    @classmethod
    def instance(cls, *args, **kw):
        if cls._singleton_instance is None:
            cls(*args, **kw)
        return cls._singleton_instance
