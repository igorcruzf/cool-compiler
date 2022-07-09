from BNFType import BNFType
from TokenType import TokenType


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


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.actual_token = self.get_next_token()
        self.tree = []

    def get_next_token(self):
        self.actual_token = self.tokens[self.token_index]
        self.token_index += 1
        return self.actual_token

    def match(self, token_type):
        if self.actual_token.type == token_type:
            token = self.actual_token
            self.get_next_token()
            return token
        else:
            raise Exception(f"Erro no token {self.actual_token.value} na linha {self.actual_token.line}"
                            f", posição {self.actual_token.position}"
                            f", token esperado {token_type.name}")

    def match_and_append(self, token_type, node):
        token = self.match(token_type)
        node.children.append(token)

    def final_match_and_append(self, token_type, node):
        if self.actual_token.type == token_type:
            token = self.actual_token
            node.children.append(token)
        else:
            raise Exception(f"Erro no token {self.actual_token.value} na linha {self.actual_token.line}"
                            f", posição {self.actual_token.position}"
                            f", token esperado {token_type.name}")

    def program(self):
        node = Node(BNFType.PROGRAM)
        while self.token_index < len(self.tokens):
            node.children.append(self.clazz())
        return node

    def clazz(self):
        node = Node(BNFType.CLASS)
        self.match_and_append(TokenType.CLASS, node)
        self.match_and_append(TokenType.TYPE, node)

        inheritance_node = self.inheritance()
        if inheritance_node is not None:
            node.children.append(inheritance_node)

        self.match_and_append(TokenType.LEFT_CURLY_BRACE, node)

        features_list_node = self.features_list()
        if features_list_node is not None:
            node.children.append(features_list_node)

        self.match_and_append(TokenType.RIGHT_CURLY_BRACE, node)
        if self.token_index == len(self.tokens):
            self.final_match_and_append(TokenType.SEMI_COLON, node)
        else:
            self.match_and_append(TokenType.SEMI_COLON, node)
        return node

    def inheritance(self):
        node = Node(BNFType.INHERITANCE)
        if self.actual_token.type == TokenType.INHERITS:
            self.match(TokenType.INHERITS)
            token = self.match(TokenType.TYPE)
            node.children.append(token)
            return node
        return None

    def features_list(self):
        node = Node(BNFType.FEATURE_LIST)
        while self.actual_token.type == TokenType.ID:
            node.children.append(self.feature())
            self.match_and_append(TokenType.SEMI_COLON, node)
        if len(node.children) == 0:
            return None
        return node

    def feature(self):
        node = Node(BNFType.FEATURE)
        self.match_and_append(TokenType.ID, node)
        if self.actual_token.type == TokenType.COLON:
            return self.formal(node)

        self.match_and_append(TokenType.LEFT_PARENTHESIS, node)
        formal_params_list_node = self.formal_params_list()
        if formal_params_list_node is not None:
            node.children.append(formal_params_list_node)
        self.match_and_append(TokenType.RIGHT_PARENTHESIS, node)
        self.match_and_append(TokenType.COLON, node)

        if self.actual_token.type == TokenType.SELF_TYPE:
            self.match_and_append(TokenType.SELF_TYPE, node)
        else:
            self.match_and_append(TokenType.TYPE, node)

        self.match_and_append(TokenType.LEFT_CURLY_BRACE, node)

        node.children.append(self.expression())
        self.match_and_append(TokenType.RIGHT_CURLY_BRACE, node)
        return node

    def formal(self, node):
        node.name = BNFType.FORMAL
        self.match_and_append(TokenType.COLON, node)
        if self.actual_token.type == TokenType.SELF_TYPE:
            self.match_and_append(TokenType.SELF_TYPE, node)
        else:
            self.match_and_append(TokenType.TYPE, node)
        if self.actual_token.type == TokenType.ASSIGN:
            self.match_and_append(TokenType.ASSIGN, node)
            node.children.append(self.expression())
        return node

    def formal_params_list(self):
        if self.actual_token.type != TokenType.ID:
            return None

        node = Node(BNFType.FORMAL_PARAM_LIST)
        node.children.append(self.formal_param())
        while self.actual_token.type == TokenType.COMMA:
            self.match_and_append(TokenType.COMMA, node)
            node.children.append(self.formal_param())
        return node

    def formal_param(self):
        node = Node(BNFType.FORMAL_PARAM)
        self.match_and_append(TokenType.ID, node)
        self.match_and_append(TokenType.COLON, node)
        if self.actual_token.type == TokenType.SELF_TYPE:
            self.match_and_append(TokenType.SELF_TYPE, node)
        else:
            self.match_and_append(TokenType.TYPE, node)
        return node

    def expression(self):
        node = Node(BNFType.EXPRESSION)
        token_type = self.actual_token.type
        if token_type == TokenType.ID:
            self.match_and_append(TokenType.ID, node)
            if self.actual_token.type == TokenType.ASSIGN:
                self.match_and_append(TokenType.ASSIGN, node)
                node.children.append(self.expression())
            elif self.actual_token.type == TokenType.LEFT_PARENTHESIS:
                node.children.append(self.argument_list_opt())
                if self.actual_token.type == TokenType.DOT:
                    node.children.append(self.expression_line())
            else:
                expression_line_node = self.expression_line()
                if expression_line_node is not None:
                    node.children.append(expression_line_node)
        elif token_type == TokenType.CASE:
            node.children.append(self.case())
        elif token_type == TokenType.IF:
            node.children.append(self.if_then_else())
        elif token_type == TokenType.WHILE:
            node.children.append(self.while_expression())
        elif token_type == TokenType.LEFT_CURLY_BRACE:
            node.children.append(self.block_expression())
        elif token_type == TokenType.LET:
            node.children.append(self.let_expression())
        elif token_type == TokenType.NEW:
            self.match_and_append(TokenType.NEW, node)
            self.match_and_append(TokenType.TYPE, node)
        elif token_type == TokenType.ISVOID:
            self.match_and_append(TokenType.ISVOID, node)
            node.children.append(self.expression())
        elif token_type == TokenType.TILDE:
            self.match_and_append(TokenType.TILDE, node)
            node.children.append(self.expression())
        elif token_type == TokenType.NOT:
            self.match_and_append(TokenType.NOT, node)
            node.children.append(self.expression())
        elif token_type == TokenType.LEFT_PARENTHESIS:
            self.match_and_append(TokenType.LEFT_PARENTHESIS, node)
            node.children.append(self.expression())
            self.match_and_append(TokenType.RIGHT_PARENTHESIS, node)
            if self.actual_token.type == TokenType.DOT:
                node.children.append(self.expression_line())
        else:
            node.children.append(self.expression_a())
            expression_line_node = self.expression_line()
            if expression_line_node is not None:
                node.children.append(expression_line_node)
        return node

    def case(self):
        node = Node(BNFType.CASE)
        self.match_and_append(TokenType.CASE, node)
        node.children.append(self.expression())
        self.match_and_append(TokenType.OF, node)
        node.children.append(self.actions())
        self.match_and_append(TokenType.ESAC, node)
        return node

    def actions(self):
        node = Node(BNFType.ACTIONS)
        node.children.append(self.action())
        while self.actual_token.type == TokenType.ID:
            node.children.append(self.action())
        return node

    def action(self):
        node = Node(BNFType.ACTION)
        self.match_and_append(TokenType.ID, node)
        self.match_and_append(TokenType.COLON, node)
        if self.actual_token.type == TokenType.SELF_TYPE:
            self.match_and_append(TokenType.SELF_TYPE, node)
        else:
            self.match_and_append(TokenType.TYPE, node)
        self.match_and_append(TokenType.BRANCH, node)
        node.children.append(self.expression())
        self.match_and_append(TokenType.SEMI_COLON, node)
        return node

    def if_then_else(self):
        node = Node(BNFType.IF_THEN_ELSE)
        self.match_and_append(TokenType.IF, node)
        node.children.append(self.expression())
        self.match_and_append(TokenType.THEN, node)
        node.children.append(self.expression())
        self.match_and_append(TokenType.ELSE, node)
        node.children.append(self.expression())
        self.match_and_append(TokenType.FI, node)
        return node

    def while_expression(self):
        node = Node(BNFType.WHILE)
        self.match_and_append(TokenType.WHILE, node)
        node.children.append(self.expression())
        self.match_and_append(TokenType.LOOP, node)
        node.children.append(self.expression())
        self.match_and_append(TokenType.POOL, node)
        return node

    def block_expression(self):
        node = Node(BNFType.BLOCK_EXPRESSION)
        self.match_and_append(TokenType.LEFT_CURLY_BRACE, node)
        node.children.append(self.expression())
        self.match_and_append(TokenType.SEMI_COLON, node)
        while self.actual_token.type != TokenType.RIGHT_CURLY_BRACE:
            node.children.append(self.expression())
            self.match_and_append(TokenType.SEMI_COLON, node)
        self.match_and_append(TokenType.RIGHT_CURLY_BRACE, node)
        return node

    def let_expression(self):
        node = Node(BNFType.LET_EXPRESSION)
        self.match_and_append(TokenType.LET, node)
        self.match_and_append(TokenType.ID, node)
        node.children.append(self.formal(Node(BNFType.FORMAL)))
        while self.actual_token.type == TokenType.COMMA:
            self.match_and_append(TokenType.ID, node)
            node.children.append(self.formal(Node(BNFType.FORMAL)))
        self.match_and_append(TokenType.IN, node)
        node.children.append(self.expression())
        return node

    def expression_a(self):
        node = Node(BNFType.EXPRESSION_A)
        token_type = self.actual_token.type
        if token_type == TokenType.SELF or token_type == TokenType.ID \
                or token_type == TokenType.INTEGER or token_type == TokenType.STRING \
                or token_type == TokenType.TRUE or token_type == TokenType.FALSE:
            self.match_and_append(token_type, node)
        else:
            self.match_and_append(TokenType.SELF, node)
        return node

    def expression_line(self):
        node = Node(BNFType.EXPRESSION_LINE)
        token_type = self.actual_token.type
        if token_type == TokenType.PLUS \
                or token_type == TokenType.MINUS or token_type == TokenType.TIMES \
                or token_type == TokenType.OVER or token_type == TokenType.LESS_THAN \
                or token_type == TokenType.LESS_EQUAL or token_type == TokenType.EQUAL:
            self.match_and_append(token_type, node)
            node.children.append(self.expression())
            expression_line_node = self.expression_line()
            if expression_line_node is not None:
                node.children.append(expression_line_node)
        elif token_type == TokenType.TYPE or token_type == TokenType.SELF_TYPE:
            self.match_and_append(token_type, node)
            self.expression_line_in_dot(node)
            while self.actual_token.type == TokenType.DOT:
                self.expression_line_in_dot(node)
        elif token_type == TokenType.DOT:
            while self.actual_token.type == TokenType.DOT:
                self.expression_line_in_dot(node)
        else:
            return None
        return node

    def argument_list_opt(self):
        node = Node(BNFType.ARGUMENT_LIST_OPT)
        self.match_and_append(TokenType.LEFT_PARENTHESIS, node)
        if self.actual_token.type != TokenType.RIGHT_PARENTHESIS:
            node.children.append(self.expression())
            while self.actual_token.type == TokenType.COMMA:
                self.match_and_append(TokenType.COMMA, node)
                node.children.append(self.expression())
        self.match_and_append(TokenType.RIGHT_PARENTHESIS, node)
        return node

    def expression_line_in_dot(self, node):
        self.match_and_append(TokenType.DOT, node)
        self.match_and_append(TokenType.ID, node)
        node.children.append(self.argument_list_opt())
        expression_line_node = self.expression_line()
        if expression_line_node is not None:
            node.children.append(expression_line_node)

    def parse(self):
        return self.program()
