from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pprint import pformat

def pp(obj):
    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()))
