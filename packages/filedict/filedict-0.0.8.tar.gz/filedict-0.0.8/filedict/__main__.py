# coding: utf-8

# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

import sys
import ctypes
import argparse
import collections

import version
import base_storage
import base_sharded_storage


TYPES = collections.OrderedDict([
    ('uint8', ctypes.c_uint8),
    ('uint16', ctypes.c_uint16),
    ('uint32', ctypes.c_uint32),
    ('uint64', ctypes.c_uint64),

    ('int8', ctypes.c_int8),
    ('int16', ctypes.c_int16),
    ('int32', ctypes.c_int32),
    ('int64', ctypes.c_int64),

    ('float32', ctypes.c_float),
    ('float64', ctypes.c_double),
    ('float80', ctypes.c_longdouble)
])

parser = argparse.ArgumentParser(
    prog='python -mfiledict',
    description='Filedict CLI.'
)
parser.add_argument(
    '-p', '--path', metavar='PATH', dest='path', action='store',
    help='Path to database.', required=True
)
parser.add_argument(
    '-m', '--max-records', metavar='N', dest='max_records', action='store',
    type=int, help='Maximum number of records in database (or in shard).',
    required=True
)
parser.add_argument(
    '-k', '--key-type', metavar='TYPE', dest='key_type', required=True,
    action='append', default=None, choices=TYPES.keys(),
    help='Key element type. Can be used multiple times.'
         ' Possible values: ' + ', '.join(TYPES.keys()) + '.'
)
parser.add_argument(
    '-v', '--value-type', metavar='TYPE', dest='val_type', required=True,
    action='append', default=None, choices=TYPES.keys(),
    help='Value element type. Can be used multiple times.'
         ' Possible values: ' + ', '.join(TYPES.keys()) + '.'
)
parser.add_argument(
    '-s', '--sharded', dest='sharded', action='store_true',
    help='Enable sharding.'
)
parser.add_argument(
    '-r', '--read-only', dest='read_only', action='store_true',
    help='Enable sharding.'
)
parser.add_argument(
    '-R', '--read_count', metavar='N', type=int, dest='read_count',
    action='store', default=100,
    help='Chunk size for read operation (in records). Default: 100.'
)
parser.add_argument(
    '-V', '--version', action='version', version=version.__version__
)

subparsers = parser.add_subparsers(dest='command', help='Possible commands.')
add_parser = subparsers.add_parser(
    'add',
    help='Read records from stdin line by line and add them to database. '
         'Line separator: new line. Items separator: space. '
         'Order of items: key items first, value items next. For example: '
         'echo "1 2 3.5" | python -mfiledict -p db -m 1000 -k uint8 -k uint16 '
         '-v float32 add'
)
add_parser = subparsers.add_parser(
    'list',
    help='Read keys from stdin line by line and list key-value pairs for these'
         'keys. Line separator: new line. Items separator: space. Example: '
         'echo "1 2" | python -mfiledict -p db -m 1000 -k uint8 -k uint16 '
         '-v float32 list. Note: is stdin is empty, list entire database. For '
         'example: python -mfiledict -p db -m 1000 -k uint8 -k uint16 '
         '-v float32 list'
)
add_parser = subparsers.add_parser(
    'del',
    help='Read keys or key-values from stdin line by line and delete them '
         'from database. Line separator: new line. Items separator: space. '
         'Order of items: key items first, value items next. For example: '
         'echo "1 2 3.5" | python -mfiledict -p db -m 1000 -k uint8 -k uint16 '
         '-v float32 add'
)
add_parser = subparsers.add_parser(
    'copy',
    help='Read records from stdin line by line and add them to database. '
         'Line separator: new line. Items separator: space. '
         'Order of items: key items first, value items next. For example: '
         'echo "1 2 3.5" | python -mfiledict -p db -m 1000 -k uint8 -k uint16 '
         '-v float32 add'
)
defragmentation_parser = subparsers.add_parser(
    'def',
    help='Run defragmentation for database. Note: this operation is very slow!'
)



args = parser.parse_args()

if args.sharded:
    base_class = base_sharded_storage.BaseShardedStorage
else:
    base_class = base_storage.BaseStorage

key_types = [TYPES[t] for t in args.key_type]
val_types = [TYPES[t] for t in args.val_type]

Storage = base_storage.storage_factory(
    base_class,
    args.max_records,
    key_types,
    val_types
)


def S():
    return Storage(args.path, args.read_only, args.read_count)

if args.command == 'add':
    with S() as db:
        for line in sys.stdin:
            line = line.strip().split()
            key, val = [], []
            for item, type_name in zip(line, args.key_type):
                if 'int' in type_name:
                    key.append(int(item))
                elif 'float' in type_name:
                    key.append(float(item))
            for item, type_name in zip(line[len(key):], args.val_type):
                if 'int' in type_name:
                    val.append(int(item))
                elif 'float' in type_name:
                    val.append(float(item))
            db.add(key, val)
elif args.command == 'def':
    with S() as db:
        db.defragmentation()
