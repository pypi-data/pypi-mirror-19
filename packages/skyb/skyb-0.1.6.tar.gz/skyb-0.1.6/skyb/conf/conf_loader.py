# coding: utf-8

import os, os.path
import re
import logging
from ..utils import asbool


class TagHandler(object):
    """
    configuration tag handler
    """

    def __init__(self, ctx=None):
        self.ctx = ctx

    def handle(self, line, ctx):
        raise NotImplementedError()


class IncludeTagHandler(TagHandler):
    def handle(self, line, ctx=None):
        if ctx is None:
            ctx = self.ctx
        assert ctx is not None
        filename = line.split()[1].strip()

        ctx.fill_file(os.path.join(os.path.dirname(ctx.current_file), filename), root=False)


class ConfigurationContext(object):
    """
    properties configuration loader

    support include
    """

    def __init__(self, strict=False):
        self._locked = False
        self.strict = strict
        self._inner_value = {}
        self.current_file = None

        self._tag_handlers = {
            "include": IncludeTagHandler()
        }

        self._error_count = 0

    def _check_lock(self):
        if self._locked:
            raise Exception("configuration is locked, cannot modify any more")

    def fill_line(self, line):
        self._check_lock()
        line = line.strip()
        if len(line) == 0:
            return

        if line.startswith('@'):
            # tag
            self._handle_tag(line)
        elif line.startswith("#"):
            # comment
            pass
        else:
            try:
                key, value = re.split("=|:", line, 1)
                self.fill_kv(key.strip(), value.strip())
            except Exception, e:
                if self.strict:
                    self._error_count += 1
                    logging.error("line: %s\t%s" % (line, e,))

        return self

    def add_tag_handler(self, name, tag_handler):
        self._tag_handlers[name] = tag_handler

    def _handle_tag(self, line):
        if len(line) < 2:
            return
        tag_indicator = line[1:].split()[0].strip()
        self._tag_handlers[tag_indicator].handle(line, ctx=self)

    def fill_file(self, filename, root=True):
        self._check_lock()
        assert os.path.exists(filename) and os.path.isfile(filename), "conf file %s not exist" % filename
        self.current_file = filename
        with open(filename, 'r') as fp:
            for line in fp:
                self.fill_line(line)

        if root and self._error_count > 0:
            raise Exception("encounter %s errors when parse config file" % self._error_count)
        return self

    def fill_kv(self, key, val, only_absent=False):
        self._check_lock()
        if only_absent and key in self._inner_value:
            return self
        self._inner_value[key] = val
        return self

    def fill_dict(self, dic, only_absent=False):
        self._check_lock()
        if not isinstance(dic, dict):
            return self
        for k, v in dic.iteritems():
            self.fill_kv(k, v, only_absent=only_absent)
        return self

    @staticmethod
    def _resolve_key_prefix(key, prefix):
        if prefix is None:
            return key
        return '%s.%s' % (prefix, key,)

    def get(self, key, default=None):
        return self._inner_value.get(key, default)

    def get_int(self, key, default=None):
        return int(self.get(key, default))

    def get_bool(self, key, default=None):
        value = self.get(key, default)
        return asbool(value)

    def mget(self, *keys, **kw):
        prefix = kw.get("prefix", None)
        values = []
        for key in keys:
            values.append(self.get(self._resolve_key_prefix(key, prefix)))
        return tuple(values)

    def lock(self):
        self._locked = True
        return self

    def get_inner_value(self):
        return self._inner_value

    def __str__(self):
        return str(self._inner_value)

    __repr__ = __str__


def load_configuration(filename, base_dir=None):
    assert filename is not None, "filename should not be None"
    assert len(filename) > 0
    if base_dir is not None:
        filename = os.path.join(base_dir, filename)
    filename = os.path.abspath(filename)
    return ConfigurationContext(strict=True).fill_file(filename)
