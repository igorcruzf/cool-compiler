class Token:
    def __init__(self, value, line, position, token_type=None):
        self.value = value
        self.type = token_type
        self.line = line + 1
        self.position = position

    def __str__(self, level=0):
        ret = "\t" * level + self.value + "\n"
        return ret
