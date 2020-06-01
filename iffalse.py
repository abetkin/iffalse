import ast
from dataclasses import dataclass
from linecache import getlines
from typing import TypedDict

from cached_property import cached_property as cached
from inspect import currentframe, getframeinfo

from traverser import Visitor


class Table:
    id: int
    value: str

@dataclass
class Qu(dict):
    tables: dict
    fields: dict


class QQ(Qu):
    def __bool__(self):
        self.__class__ = self.__class__.__mro__[1]
        return False


def query():
    obj = Query(currentframe().f_back)
    return obj.query

class Query():
    def __init__(self, frame):
        self.frame = frame

    @cached
    def query(self):
        node = ast.parse(self.definition)
        visitor = Visitor()
        visitor.visit(node)
        tables = visitor.tables
        for alias, table in tuple(tables.items()):
            tables[alias] = eval(table, self.frame.f_globals, self.frame.f_locals)
        return QQ(**{'tables': tables, 'fields': visitor.fields})

    @cached
    def definition(self):
        offset = None
        fragment = []
        lines = getlines(self.filename)
        for i, line in enumerate(lines):
            if i < self.lineno:
                continue
            num_spaces, line = self._dedent(line)
            if offset is None:
                offset = num_spaces
                fragment.append(line)
            elif num_spaces >= offset:
                fragment.append(line)
            else:
                break
        return ''.join(fragment)

    @cached
    def lineno(self):
        frameinfo = getframeinfo(self.frame)
        return frameinfo.lineno

    @cached
    def filename(self):
        frameinfo = getframeinfo(self.frame)
        return frameinfo.filename

    def _dedent(self, string):
        for i, char in enumerate(string):
            if not char.isspace():
                break
        return i, string[i:]



if __name__ == '__main__':
    if qu := query():
        t: Table
        t.id, t.value

    print(qu.data)