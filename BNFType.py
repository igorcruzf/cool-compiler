import enum


class BNFType(enum.Enum):
    PROGRAM = 0,
    CLASS = 1,
    INHERITANCE = 2,
    FEATURE_LIST = 3,
    FEATURE = 4,
    FORMAL = 5,
    FORMAL_PARAM_LIST = 6,
    FORMAL_PARAM = 7,
    EXPRESSION = 8,
    CASE = 9,
    ACTIONS = 10,
    ACTION = 11,
    IF_THEN_ELSE = 12,
    WHILE = 13,
    BLOCK_EXPRESSION = 14,
    LET_EXPRESSION = 15,
    EXPRESSION_A = 16,
    EXPRESSION_LINE = 17,
    ARGUMENT_LIST_OPT = 18


