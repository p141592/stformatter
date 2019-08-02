import uuid

from parser import ALLOW_TYPES
from tree.mixins import TreeLenMixin


class BaseTree(TreeLenMixin):
    def __init__(self, *args,
                 parent=None,
                 content=None,
                 **kwargs
                 ):
        self.id = uuid.uuid4()
        self.children = []
        self.parent = parent
        self.hash = None
        self.content = content

    def __str__(self):
        result = [f'HEAD: {self.type}:{self.id}: {hash(self)}']
        if self.content:
            result.append(f'CONTENT: {self.content}\n')
        if self.children:
            result.append(f'CHILDREN_LENGTH: {len(self.children)}')

        return "\n".join(result)

    def get_parent(self, parent_type):
        assert parent_type in ALLOW_TYPES, f"Указанный тип родителя \"{parent_type}\" запрещен"
        if self.type == parent_type:
            return self

        if self.parent:
            return self.parent.get_parent(parent_type)

    def search(self, term):
        if self.content and self.content == term:
            print(f'{self.get_parent("DOCUMENT").filename}: {self.get_parent("LINE").offset}')

        for _child in self.children:
            _child.search(term)

    def set_type(self, type):
        if type in ALLOW_TYPES and self.type != type:
            self.type = type


    def get_line(self, number):
        if self.offset:
            return self

        for _child in self.children:
            result = _child.get_line(number)
            if result:
                return result

    def append(self, node):
        node.parent = self
        self.hash = None
        self.children.append(node)