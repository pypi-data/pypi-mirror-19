import sys

PY2 = sys.version_info[0] == 2

if PY2:
    get_input = raw_input
else:
    get_input = input
