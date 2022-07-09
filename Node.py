class Node:
    def __init__(self, token, children=None):
        if children is None:
            children = []
        self.name = token
        self.children = children

    def __str__(self, level=0):
        ret = "\t" * level + self.name.name + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret
