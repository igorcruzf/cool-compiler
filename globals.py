
# Using enum class create enumerations
import enum


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
    TRUE = 15,
    FALSE = 16,

    # multicharacter tokens
    ID = 17,
    TYPE = 18,
    INTEGER = 19,
    STRING = 20,
    SELF = 21,
    SELF_TYPE = 22,

    # special symbols
    LEFT_PARENTHESIS = 24,
    RIGHT_PARENTHESIS = 25,
    SEMI_COLON = 26,
    LEFT_CURLY_BRACE = 39,
    RIGHT_CURLY_BRACE = 40,
    COLON = 41,
    DOT = 42

    # Binary op  +|-|*|/|<-|<|<=|=
    PLUS = 27,
    MINUS = 28,
    TIMES = 29,
    OVER = 30,
    ASSIGN = 31,
    LESS_THAN = 32,
    LESS_EQUAL = 33,
    EQUAL = 34

    # Unary op ~|isvoid|not
    TILDE = 35,
    NOT = 36,
    ISVOID = 37,

    # COMMENT
    COMMENT = 38
