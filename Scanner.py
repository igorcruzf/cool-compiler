from Token import Token
from TokenType import TokenType
from vars import EOF, reserved_words, case_sensitive_words, boolean_words, special_symbols, less_operators


class Scanner:

    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.line_buff = self.file.readline()
        self.line_index = 0

    def move_to_next_char(self):
        if not self.line_buff:
            raise Exception("M=move_to_next_char, tentando mover para próximo caracter após EOF.")

        if self.line_index == len(self.line_buff):
            self.line_buff = self.file.readline()
            if not self.line_buff:
                return EOF
            self.line_index = 0
        self.line_index += 1

    def get_next_char(self):
        if not self.line_buff:
            raise Exception("M=get_next_char, tentando pegar próximo caracter após EOF.")

        if self.line_index == len(self.line_buff):
            self.line_buff = self.file.readline()
            if not self.line_buff:
                return EOF
            self.line_index = 0
        self.line_index += 1
        return self.line_buff[self.line_index - 1]

    def peek_next_char(self):
        if not self.line_buff:
            raise Exception("M=peek_next_char, tentando olhar próximo caracter após EOF.")
        return self.line_buff[self.line_index]

    def in_integer(self, integer_token):
        c = self.peek_next_char()
        while c.isnumeric():
            integer_token.value += c
            self.move_to_next_char()
            c = self.peek_next_char()

    def in_id_or_type(self, id_type_token):
        c = self.peek_next_char()
        while c.isalnum() or c == "_":
            id_type_token.value += c
            self.move_to_next_char()
            c = self.peek_next_char()

    def in_string(self, string_token):
        c = self.peek_next_char()
        while c != "\"":
            string_token.value += c
            self.move_to_next_char()
            c = self.peek_next_char()
        string_token.value += c
        self.move_to_next_char()

    @staticmethod
    def is_reserved_word(token):
        token.type = reserved_words.get(token.value.lower(), token.type)

    @staticmethod
    def is_case_sensitive_word(token):
        token.type = case_sensitive_words.get(token.value, token.type)

    @staticmethod
    def is_boolean(token):
        if token.value[0].islower():
            token.type = boolean_words.get(token.value, token.type)

    @staticmethod
    def is_special_symbol(token):
        token.type = special_symbols.get(token.value, None)

    def in_single_line_comment(self, comment_token):
        c = self.get_next_char()
        while c != '\n' and c != EOF:
            comment_token.value += c
            c = self.get_next_char()

    def in_minus(self, token):
        c = self.peek_next_char()
        if c == "-":
            token.value += c
            self.move_to_next_char()
            token.type = TokenType.COMMENT
            self.in_single_line_comment(token)
        else:
            token.type = TokenType.MINUS

    def in_multi_line_comment(self, comment_token):
        c = self.get_next_char()
        is_last_char_asterisk = False
        while not (c == ")" and is_last_char_asterisk):
            comment_token.value += c
            if c == "*":
                is_last_char_asterisk = True
            else:
                is_last_char_asterisk = False
            c = self.get_next_char()
        comment_token.value += c

    def in_left_parenthesis(self, token):
        next_char = self.peek_next_char()
        if next_char == "*":
            token.value += next_char
            self.move_to_next_char()
            token.type = TokenType.COMMENT
            self.in_multi_line_comment(token)
        else:
            token.type = TokenType.LEFT_PARENTHESIS

    def in_less_operators(self, token):
        next_char = self.peek_next_char()
        token.type = less_operators.get("<" + next_char, TokenType.LESS_THAN)
        if token.type != TokenType.LESS_THAN:
            token.value += next_char
            self.move_to_next_char()

    @staticmethod
    def has_to_ignore(c):
        return c == '\n' or c == ' ' or c == '\t' or c == EOF

    def get_all_tokens(self):
        all_tokens = []
        while self.line_buff:
            token = self.get_token()
            if token is not None:
                print(f"""value = {token.value}, type = {token.type}""")
                all_tokens.append(token)
        
        return all_tokens

    def get_token(self):
        c = self.get_next_char()
        if self.has_to_ignore(c):
            return None

        token = Token(c)
        if c.isnumeric():
            token.type = TokenType.INTEGER
            self.in_integer(token)
        elif c.isalpha():
            if c.islower():
                token.type = TokenType.ID
            else:
                token.type = TokenType.TYPE
            self.in_id_or_type(token)
            self.is_boolean(token)
            self.is_reserved_word(token)
            self.is_case_sensitive_word(token)
        elif c == "\"":
            token.type = TokenType.STRING
            self.in_string(token)
        elif c == "(":
            self.in_left_parenthesis(token)
        elif c == "-":
            self.in_minus(token)
        elif c == "<":
            self.in_less_operators(token)
        else:
            self.is_special_symbol(token)
            if token.type is None:
                raise Exception(f"""ISSO NÃO PODE ACONTECER, token={token.value}""")

        return token