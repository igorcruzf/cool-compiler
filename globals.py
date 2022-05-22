import globals


# Using enum class create enumerations
class TokenType(enum.Enum):
    # reserved words
    CLASS = 0,
    INHERITS = 1,
    IF = 2,
    THEN = 3,
    ELSE = 4,
    FI = 5,
    WHILE = 6,
    LOOP = 7,
    POOL = 8,
    LET = 9,
    IN = 10,
    CASE = 11,
    OF = 12,
    ESAC = 13,
    NEW = 14,
    ISVOID = 15,
    NOT = 16,
    TRUE = 17,
    FALSE = 18,

    # multicharacter tokens
    ID = 19,
    TYPE = 20,
    INTEGER = 21,
    STRING = 22,
    SPECIAL_ID = 23,
    ID = 24,
    NUM = 25,

    # special symbols
    LPAREN = 26,
    RPAREN = 27,
    SEMI = 28

    # Binary op  +|-|*|/|<-|<|<=|=
    PLUS = 29,
    MINUS = 30,
    TIMES = 31,
    OVER = 32,
    ASSIGN = 33,
    LESSTHAN = 34,
    LESSEQUAL = 35,
    EQUAL = 36

    # Unary op ~|isvoid|not
    TILDE = 37,
    NOT = 38,
    ISVOID = 39
