import ast
from cached_property import cached_property as cached
from inspect import currentframe, getframeinfo

from traverser import Visitor


class Table:
    id: int
    value: str


class query:
    data = None

    def __init__(self):
        self.frame = currentframe().f_back

    def __bool__(self):
        if self.data:
            return super().__bool__()
        self.data = self._fetch()
        return False

    def _fetch(self):
        return self.query

    @cached
    def query(self):
        node = ast.parse(self.definition)
        visitor = Visitor()
        visitor.visit(node)
        tables = visitor.tables
        for alias, table in tuple(tables.items()):
            tables[alias] = eval(table, self.frame.f_globals, self.frame.f_locals)
        return {
            'tables': tables, 'fields': visitor.fields
        }

    @cached
    def definition(self):
        offset = None
        fragment = []
        with open(self.filename) as f:
            for i, line in enumerate(f.readlines()):
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