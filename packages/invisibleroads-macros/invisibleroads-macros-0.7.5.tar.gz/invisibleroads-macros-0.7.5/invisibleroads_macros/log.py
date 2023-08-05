from __future__ import print_function

try:
    from logging import NullHandler
except ImportError:  # Python 2.6
    from logging import Handler

    class NullHandler(Handler):

        def emit(self, record):
            pass
finally:
    from logging import getLogger

import re
import traceback
from collections import OrderedDict
from os.path import expanduser
from six import string_types
from sys import stderr

from .disk import COMMAND_LINE_HOME


def get_log(name):
    log = getLogger(name)
    log.addHandler(NullHandler())
    return log


def filter_nested_dictionary(value_by_key, f):
    d = OrderedDict()
    for k, v in value_by_key.items():
        if f(k):
            continue
        if hasattr(v, 'items'):
            v = filter_nested_dictionary(v, f)
        d[k] = v
    return d


def print_error(x, *args):
    'Print to standard error stream'
    print(x % args, file=stderr)


def stylize_dictionary(value_by_key, suffix_format_packs):
    d = {}
    for key, value in value_by_key.items():
        for suffix, format_value in suffix_format_packs:
            if key.endswith(suffix):
                value = format_value(value)
                break
        d[key] = value
    return d


def format_summary(value_by_key, suffix_format_packs=None):
    format_by_suffix = OrderedDict([
        ('_folder', format_path),
        ('_path', format_path),
    ] + (suffix_format_packs or []))
    return format_nested_dictionary(OrderedDict(
        value_by_key), format_by_suffix.items())


def format_nested_dictionary(
        value_by_key, suffix_format_packs=None, prefix=''):
    parts = []
    for key, value in value_by_key.items():
        left_hand_side = prefix + str(key)
        if hasattr(value, 'items'):
            parts.append(format_nested_dictionary(
                value, suffix_format_packs, left_hand_side + '.'))
            continue
        for suffix, format_value in suffix_format_packs or []:
            if key.endswith(suffix):
                parts.append(left_hand_side + ' = ' + format_value(value))
                break
        else:
            if not isinstance(value, string_types):
                value = str(value)
            if '\n' in value:
                value = format_indented_block(value)
            parts.append(left_hand_side + ' = ' + value)
    return '\n'.join(parts)


def format_path(x):
    return re.sub(r'^' + expanduser('~'), COMMAND_LINE_HOME, x)


def format_hanging_indent(x):
    lines = x.strip().splitlines()
    if not lines:
        return ''
    if len(lines) == 1:
        return lines[0]
    return lines[0] + '\n' + '\n'.join('  ' + line for line in lines[1:])


def format_indented_block(x):
    return '\n' + '\n'.join('  ' + line for line in x.strip().splitlines())


def get_nested_dictionary(nested_lists):
    d = OrderedDict()
    for k, v in nested_lists:
        if k.endswith('_'):
            try:
                v = get_nested_dictionary(v)
            except TypeError:
                pass
            else:
                k = k[:-1]
        d[k] = v
    return d


def get_nested_lists(nested_dictionary):
    xs = []
    for k, v in nested_dictionary.items():
        if hasattr(v, 'items'):
            v = get_nested_lists(v)
            k = k + '_'
        xs.append((k, v))
    return xs


def parse_nested_dictionary_from(raw_dictionary, max_depth=float('inf')):
    value_by_key = OrderedDict()
    for key, value in OrderedDict(raw_dictionary).items():
        key_parts = key.split('.')
        d = value_by_key
        depth = 0
        while key_parts:
            key_part = key_parts.pop(0)
            if len(key_parts) and depth < max_depth:
                if key_part not in d:
                    d[key_part] = OrderedDict()
                d = d[key_part]
                depth += 1
            else:
                d['.'.join([key_part] + key_parts)] = value
                break
    return value_by_key


def parse_nested_dictionary(text, is_key=lambda x: True):
    raw_dictionary, key = OrderedDict(), None
    for line in text.splitlines():
        if line.startswith('  '):
            if key is not None:
                value = line[2:].rstrip()
                raw_dictionary[key].append(value)
            continue
        try:
            key, value = line.split(' = ', 1)
            if not is_key(key):
                key = None
        except ValueError:
            key = None
        if not key:
            continue
        key = key.strip()
        value = value.strip()
        raw_dictionary[key] = [value]
    d = OrderedDict()
    for k, v in raw_dictionary.items():
        this_dictionary = d
        for key in k.split('.'):
            key = key.strip()
            last_dictionary = this_dictionary
            try:
                this_dictionary = this_dictionary[key]
            except KeyError:
                this_dictionary[key] = {}
                this_dictionary = this_dictionary[key]
        last_dictionary[key] = '\n'.join(v).strip()
    return d


def log_traceback(log, d=None):
    log.error(traceback.format_exc() + str(d))
