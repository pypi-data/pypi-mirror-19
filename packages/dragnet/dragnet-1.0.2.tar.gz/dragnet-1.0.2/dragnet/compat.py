import sys

PY2 = int(sys.version[0]) == 2

if PY2:
    range_ = xrange
    bytes_ = str
    unicode_ = unicode
    string_ = (str, unicode)
else:
    range_ = range
    bytes_ = bytes
    unicode_ = str
    string_ = (bytes, str)
