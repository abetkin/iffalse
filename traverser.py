import ast
from dataclasses import dataclass, field


@dataclass()
class Visitor(ast.NodeVisitor):
    tables: dict = field(default_factory=dict)
    fields: list = field(default_factory=dict)

    def visit_AnnAssign(self, node):
        self.tables[node.target.id] = node.annotation.id

    def visit_Tuple(self, node):
        attrs = node.elts
        assert all(
            isinstance(elt, ast.Attribute) for elt in attrs
        )
        self._process_attrs(attrs)

    def _process_attrs(self, nodes):
        data = self.fields
        for node in nodes:
            alias = node.value.id
            data.setdefault(alias, []).append(node.attr)