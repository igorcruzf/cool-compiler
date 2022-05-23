from TokenType import TokenType

EOF = "EOF"

reserved_words = {
    "class": TokenType.CLASS,
    "inherits": TokenType.INHERITS,
    "if": TokenType.IF,
    "then": TokenType.THEN,
    "else": TokenType.ELSE,
    "fi": TokenType.FI,
    "while": TokenType.WHILE,
    "loop": TokenType.LOOP,
    "pool": TokenType.POOL,
    "let": TokenType.LET,
    "in": TokenType.IN,
    "case": TokenType.CASE,
    "of": TokenType.OF,
    "esac": TokenType.ESAC,
    "new": TokenType.NEW,
    "isvoid": TokenType.ISVOID,
    "not": TokenType.NOT
}

boolean_words = {
    "true": TokenType.TRUE,
    "false": TokenType.FALSE
}

case_sensitive_words = {
    "self": TokenType.SELF,
    "SELF_TYPE": TokenType.SELF_TYPE
}

special_symbols = {
    ")": TokenType.RIGHT_PARENTHESIS,
    ";": TokenType.SEMI_COLON,
    "+": TokenType.PLUS,
    "*": TokenType.TIMES,
    "/": TokenType.OVER,
    "=": TokenType.EQUAL,
    "~": TokenType.TILDE,
    "{": TokenType.LEFT_CURLY_BRACE,
    "}": TokenType.RIGHT_CURLY_BRACE,
    ":": TokenType.COLON,
    ".": TokenType.DOT,
    ",": TokenType.COMMA
}

less_operators = {
    "<-": TokenType.ASSIGN,
    "<=": TokenType.LESS_EQUAL
}