import ast
import os
from inspect import currentframe, getframeinfo


class Table:
    id: int
    value: str


class query:
    data = None

    def __init__(self):
        frame = currentframe().f_back
        frameinfo = getframeinfo(frame)
        self.lineno = frameinfo.lineno
        self.filename = frameinfo.filename

    def __bool__(self):
        if self.data:
            return super().__bool__()
        self.data = self._fetch()
        return False

    def _fetch(self):
        offset = None
        definition = []
        with open(self.filename) as f:
            for i, line in enumerate(f.readlines()):
                if i < self.lineno:
                    continue
                num_spaces, line = self._dedent(line)
                if offset is None:
                    offset = num_spaces
                    definition.append(line)
                elif num_spaces >= offset:
                    definition.append(line)
                else:
                    break
        definition = ''.join(definition)
        return ast.parse(definition)

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