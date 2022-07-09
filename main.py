from Parser import Parser
from Scanner import Scanner
from TokenType import TokenType

if __name__ == '__main__':
    tokens = Scanner("Testes.cl").get_all_tokens()
    tokens_without_comment = [token for token in tokens if token.type != TokenType.COMMENT]
    [parsed_tokens, errors] = Parser(tokens_without_comment).parse()
    print(parsed_tokens)
    [print(error) for error in errors]

