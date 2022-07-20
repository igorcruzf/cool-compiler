from BNFType import BNFType
from Node import Node
from TokenType import TokenType


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.actual_token = self.get_next_token()
        self.declared_ids = []
        self.used_ids = []
        self.tree = []
        self.errors = []

    def get_next_token(self):
        self.actual_token = self.tokens[self.token_index]
        self.token_index += 1
        return self.actual_token

    def match(self, token_type):
        if self.actual_token.type == token_type:
            if token_type == TokenType.ID:
                self.used_ids.append(self.actual_token)
            token = self.actual_token
            self.get_next_token()
            return token
        else:
            self.errors.append(f"[Erro] Token inválido {self.actual_token.value} na linha {self.actual_token.line}"
                               f", posição {self.actual_token.position}"
                               f", esperado '{token_type.name}'")

    def match_and_append(self, token_type, node):
        token = self.match(token_type)
        if token is not None:
            node.children.append(token)

    def scan_to(self, sync_tokens):
        while self.actual_token.type not in sync_tokens:
            self.get_next_token()

    def check_input(self, expected_tokens, sync_tokens):
        if self.actual_token.type not in expected_tokens:
            self.errors.append(f"[Erro] Token inválido {self.actual_token.value} na linha {self.actual_token.line}"
                               f", posição {self.actual_token.position}, esperado {[token.name for token in expected_tokens]}")
            self.scan_to(expected_tokens + sync_tokens)

    def final_match_and_append(self, token_type, node):
        if self.actual_token.type == token_type:
            token = self.actual_token
            node.children.append(token)
        else:
            self.errors.append(f"[Erro] Token inválido {self.actual_token.value} na linha {self.actual_token.line}"
                               f", posição {self.actual_token.position}"
                               f", token esperado '{token_type.name}'")

    def is_declared_id(self):
        return self.actual_token.value in self.declared_ids

    def program(self):
        node = Node(BNFType.PROGRAM)
        while self.token_index < len(self.tokens):
            node.children.append(self.clazz([TokenType.SEMI_COLON]))
        return node

    def clazz(self, sync_tokens):
        node = Node(BNFType.CLASS)
        self.check_input([TokenType.CLASS], [])
        if self.actual_token.type not in sync_tokens:
            self.match_and_append(TokenType.CLASS, node)
            self.match_and_append(TokenType.TYPE, node)

            inheritance_node = self.inheritance()
            if inheritance_node is not None:
                node.children.append(inheritance_node)

            self.match_and_append(TokenType.LEFT_CURLY_BRACE, node)

            features_list_node = self.features_list([TokenType.RIGHT_CURLY_BRACE])
            if features_list_node is not None:
                node.children.append(features_list_node)

            self.match_and_append(TokenType.RIGHT_CURLY_BRACE, node)
            if self.token_index == len(self.tokens):
                self.final_match_and_append(TokenType.SEMI_COLON, node)
            else:
                self.match_and_append(TokenType.SEMI_COLON, node)
        else:
            self.match_and_append(TokenType.SEMI_COLON, node)
        return node

    def inheritance(self):
        node = Node(BNFType.INHERITANCE)
        if self.actual_token.type == TokenType.INHERITS:
            self.match_and_append(TokenType.INHERITS, node)
            self.match_and_append(TokenType.TYPE, node)
            return node
        return None

    def features_list(self, sync_tokens):
        node = Node(BNFType.FEATURE_LIST)
        self.check_input([TokenType.ID], sync_tokens)
        if self.actual_token.type not in sync_tokens:
            while self.actual_token.type == TokenType.ID:
                self.declared_ids.append(self.actual_token.value)
                node.children.append(self.feature([TokenType.SEMI_COLON]))
                self.match_and_append(TokenType.SEMI_COLON, node)
                if self.actual_token.type != TokenType.ID:
                    self.check_input(sync_tokens, [TokenType.ID])
            if len(node.children) == 0:
                return None
            return node
        return None

    def feature(self, sync_tokens):
        node = Node(BNFType.FEATURE)
        self.check_input([TokenType.ID], sync_tokens)
        if self.actual_token.type not in sync_tokens:
            token_id = None
            if self.actual_token.type == TokenType.ID:
                token_id = self.actual_token
            self.match_and_append(TokenType.ID, node)
            if self.actual_token.type == TokenType.COLON:
                if token_id is not None:
                    self.declared_ids.append(token_id)
                return self.formal(node, sync_tokens)

            self.check_input([TokenType.LEFT_PARENTHESIS], sync_tokens)
            if self.actual_token.type not in sync_tokens:
                self.match_and_append(TokenType.LEFT_PARENTHESIS, node)
                formal_params_list_node = self.formal_params_list([TokenType.RIGHT_PARENTHESIS])
                if formal_params_list_node is not None:
                    node.children.append(formal_params_list_node)

                self.match_and_append(TokenType.RIGHT_PARENTHESIS, node)
                self.match_and_append(TokenType.COLON, node)

                if self.actual_token.type == TokenType.SELF_TYPE:
                    self.match_and_append(TokenType.SELF_TYPE, node)
                else:
                    self.match_and_append(TokenType.TYPE, node)

                self.match_and_append(TokenType.LEFT_CURLY_BRACE, node)

                node.children.append(self.expression([TokenType.RIGHT_CURLY_BRACE]))
                self.match_and_append(TokenType.RIGHT_CURLY_BRACE, node)
        return node

    def formal(self, node, sync_tokens):
        node.name = BNFType.FORMAL
        self.match_and_append(TokenType.COLON, node)
        self.check_input([TokenType.TYPE, TokenType.SELF_TYPE], sync_tokens)
        if self.actual_token.type not in sync_tokens:
            if self.actual_token.type == TokenType.SELF_TYPE:
                self.match_and_append(TokenType.SELF_TYPE, node)
            else:
                self.match_and_append(TokenType.TYPE, node)
            if self.actual_token.type == TokenType.ASSIGN:
                self.match_and_append(TokenType.ASSIGN, node)
                node.children.append(self.expression(sync_tokens))
        return node

    def formal_params_list(self, sync_tokens):
        self.check_input([TokenType.ID, TokenType.RIGHT_PARENTHESIS], sync_tokens)
        if self.actual_token.type != TokenType.ID:
            return None

        node = Node(BNFType.FORMAL_PARAM_LIST)
        node.children.append(self.formal_param([TokenType.RIGHT_PARENTHESIS, TokenType.COMMA]))
        while self.actual_token.type == TokenType.COMMA:
            self.match_and_append(TokenType.COMMA, node)
            node.children.append(self.formal_param([TokenType.RIGHT_PARENTHESIS, TokenType.COMMA]))
        return node

    def formal_param(self, sync_tokens):
        node = Node(BNFType.FORMAL_PARAM)

        if self.actual_token.type == TokenType.ID:
            self.declared_ids.append(self.actual_token.value)
        self.match_and_append(TokenType.ID, node)
        self.check_input([TokenType.COLON], sync_tokens)
        if self.actual_token.type not in sync_tokens:
            self.match_and_append(TokenType.COLON, node)
            if self.actual_token.type == TokenType.SELF_TYPE:
                self.match_and_append(TokenType.SELF_TYPE, node)
            else:
                self.match_and_append(TokenType.TYPE, node)
        return node

    def expression(self, sync_tokens):
        node = Node(BNFType.EXPRESSION)
        possible_tokens = [TokenType.ID, TokenType.CASE,
                           TokenType.IF, TokenType.WHILE, TokenType.LEFT_CURLY_BRACE,
                           TokenType.LET, TokenType.NEW, TokenType.ISVOID, TokenType.TILDE, TokenType.NOT,
                           TokenType.LEFT_PARENTHESIS, TokenType.SELF, TokenType.INTEGER, TokenType.STRING,
                           TokenType.TRUE, TokenType.FALSE]
        self.check_input(possible_tokens, sync_tokens)
        token_type = self.actual_token.type
        if token_type == TokenType.ID:
            self.match_and_append(TokenType.ID, node)
            if self.actual_token.type == TokenType.ASSIGN:
                self.match_and_append(TokenType.ASSIGN, node)
                node.children.append(self.expression([TokenType.SEMI_COLON]))
            elif self.actual_token.type == TokenType.LEFT_PARENTHESIS:
                node.children.append(self.argument_list_opt())
                if self.actual_token.type == TokenType.DOT:
                    node.children.append(self.expression_line(sync_tokens))
            else:
                expression_line_node = self.expression_line(sync_tokens)
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
            node.children.append(self.let_expression(sync_tokens))
        elif token_type == TokenType.NEW:
            self.match_and_append(TokenType.NEW, node)
            self.match_and_append(TokenType.TYPE, node)
        elif token_type == TokenType.ISVOID:
            self.match_and_append(TokenType.ISVOID, node)
            node.children.append(self.expression(sync_tokens))
        elif token_type == TokenType.TILDE:
            self.match_and_append(TokenType.TILDE, node)
            node.children.append(self.expression(sync_tokens))
        elif token_type == TokenType.NOT:
            self.match_and_append(TokenType.NOT, node)
            node.children.append(self.expression(sync_tokens))
        elif token_type == TokenType.LEFT_PARENTHESIS:
            self.match_and_append(TokenType.LEFT_PARENTHESIS, node)
            node.children.append(self.expression([TokenType.RIGHT_PARENTHESIS]))
            self.match_and_append(TokenType.RIGHT_PARENTHESIS, node)
            if self.actual_token.type == TokenType.DOT:
                node.children.append(self.expression_line(sync_tokens))
        else:
            node.children.append(self.expression_a())
            expression_line_node = self.expression_line(sync_tokens)
            if expression_line_node is not None:
                node.children.append(expression_line_node)
        return node

    def case(self):
        node = Node(BNFType.CASE)
        self.match_and_append(TokenType.CASE, node)
        node.children.append(self.expression([TokenType.OF]))
        self.match_and_append(TokenType.OF, node)
        node.children.append(self.actions([TokenType.ESAC]))
        self.match_and_append(TokenType.ESAC, node)
        return node

    def actions(self, sync_tokens):
        node = Node(BNFType.ACTIONS)
        node.children.append(self.action(sync_tokens + [TokenType.SEMI_COLON]))
        while self.actual_token.type == TokenType.ID:
            node.children.append(self.action(sync_tokens + [TokenType.SEMI_COLON]))
        return node

    def action(self, sync_tokens):
        node = Node(BNFType.ACTION)
        if self.actual_token.type == TokenType.ID:
            self.declared_ids.append(self.actual_token.value)
        self.check_input([TokenType.ID], sync_tokens)
        if self.actual_token.type not in sync_tokens:
            self.match_and_append(TokenType.ID, node)
            self.match_and_append(TokenType.COLON, node)
            if self.actual_token.type == TokenType.SELF_TYPE:
                self.match_and_append(TokenType.SELF_TYPE, node)
            else:
                self.match_and_append(TokenType.TYPE, node)
            self.match_and_append(TokenType.BRANCH, node)
            node.children.append(self.expression([TokenType.SEMI_COLON]))
            self.match_and_append(TokenType.SEMI_COLON, node)
        return node

    def if_then_else(self):
        node = Node(BNFType.IF_THEN_ELSE)
        self.match_and_append(TokenType.IF, node)
        node.children.append(self.expression([TokenType.THEN]))
        self.match_and_append(TokenType.THEN, node)
        node.children.append(self.expression([TokenType.ELSE]))
        self.match_and_append(TokenType.ELSE, node)
        node.children.append(self.expression([TokenType.FI]))
        self.match_and_append(TokenType.FI, node)
        return node

    def while_expression(self):
        node = Node(BNFType.WHILE)
        self.match_and_append(TokenType.WHILE, node)
        node.children.append(self.expression([TokenType.LOOP]))
        self.match_and_append(TokenType.LOOP, node)
        node.children.append(self.expression([TokenType.POOL]))
        self.match_and_append(TokenType.POOL, node)
        return node

    def block_expression(self):
        node = Node(BNFType.BLOCK_EXPRESSION)
        self.match_and_append(TokenType.LEFT_CURLY_BRACE, node)
        node.children.append(self.expression([TokenType.SEMI_COLON, TokenType.RIGHT_CURLY_BRACE]))
        self.match_and_append(TokenType.SEMI_COLON, node)
        while self.actual_token.type != TokenType.RIGHT_CURLY_BRACE:
            node.children.append(self.expression([TokenType.SEMI_COLON, TokenType.RIGHT_CURLY_BRACE]))
            self.match_and_append(TokenType.SEMI_COLON, node)
        self.match_and_append(TokenType.RIGHT_CURLY_BRACE, node)
        return node

    def let_expression(self, sync_tokens):
        node = Node(BNFType.LET_EXPRESSION)
        self.match_and_append(TokenType.LET, node)
        self.check_input([TokenType.ID], [TokenType.IN])
        if self.actual_token.type != TokenType.IN:
            if self.actual_token.type == TokenType.ID:
                self.declared_ids.append(self.actual_token.value)
            self.match_and_append(TokenType.ID, node)
            node.children.append(self.formal(Node(BNFType.FORMAL), [TokenType.IN, TokenType.COMMA]))
            while self.actual_token.type == TokenType.COMMA:
                if self.actual_token.type == TokenType.ID:
                    self.declared_ids.append(self.actual_token.value)
                self.match_and_append(TokenType.ID, node)
                node.children.append(self.formal(Node(BNFType.FORMAL), [TokenType.IN, TokenType.COMMA]))
        self.match_and_append(TokenType.IN, node)
        node.children.append(self.expression(sync_tokens))
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

    def expression_line(self, sync_tokens):
        node = Node(BNFType.EXPRESSION_LINE)
        token_type = self.actual_token.type
        if token_type == TokenType.PLUS \
                or token_type == TokenType.MINUS or token_type == TokenType.TIMES \
                or token_type == TokenType.OVER or token_type == TokenType.LESS_THAN \
                or token_type == TokenType.LESS_EQUAL or token_type == TokenType.EQUAL:
            self.match_and_append(token_type, node)
            node.children.append(self.expression(sync_tokens))
            expression_line_node = self.expression_line(sync_tokens)
            if expression_line_node is not None:
                node.children.append(expression_line_node)
        elif token_type == TokenType.TYPE or token_type == TokenType.SELF_TYPE:
            self.match_and_append(token_type, node)
            self.expression_line_in_dot(node, [TokenType.RIGHT_PARENTHESIS], sync_tokens)
            while self.actual_token.type == TokenType.DOT:
                self.expression_line_in_dot(node, [TokenType.RIGHT_PARENTHESIS], sync_tokens)
        elif token_type == TokenType.DOT:
            while self.actual_token.type == TokenType.DOT:
                self.expression_line_in_dot(node, [TokenType.RIGHT_PARENTHESIS], sync_tokens)
        else:
            return None
        return node

    def argument_list_opt(self):
        node = Node(BNFType.ARGUMENT_LIST_OPT)
        self.match_and_append(TokenType.LEFT_PARENTHESIS, node)
        if self.actual_token.type != TokenType.RIGHT_PARENTHESIS:
            node.children.append(self.expression([TokenType.RIGHT_PARENTHESIS, TokenType.COMMA]))
            while self.actual_token.type == TokenType.COMMA:
                self.match_and_append(TokenType.COMMA, node)
                node.children.append(self.expression([TokenType.RIGHT_PARENTHESIS, TokenType.COMMA]))
        self.match_and_append(TokenType.RIGHT_PARENTHESIS, node)
        return node

    def expression_line_in_dot(self, node, sync_tokens, line_sync_tokens):
        self.match_and_append(TokenType.DOT, node)
        self.check_input([TokenType.ID], sync_tokens)
        self.match_and_append(TokenType.ID, node)
        node.children.append(self.argument_list_opt())
        expression_line_node = self.expression_line(line_sync_tokens)
        if expression_line_node is not None:
            node.children.append(expression_line_node)

    def parse(self):
        tree = None
        try:
            tree = self.program()
        except IndexError:
            self.errors.append(f"[Erro] Fim do arquivo inesperado.")
        for token in self.used_ids:
            if token.value not in self.declared_ids:
                self.errors.append(f"[Cuidado] ID {token.value} na linha {token.line}"
                                   f", posição {token.position}"
                                   f" usado antes de ser declarado.")
        return [tree, self.errors]
