from interpreter.lexical_analysis.token import Token
from interpreter.lexical_analysis.tokenType import *


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.line_count = 1
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Unexpected character: {} | Line: {}'.format(self.current_char, self.line_count))

    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def integer(self):
        number = ''
        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        return int(number)

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
            if result == '***':
                return Token(COMMENT, '***')

        if result == 'Libraries':
            return Token(LIBRARIES, result)
        elif result == 'Functions':
            return Token(FUNCTIONS, result)
        elif result == 'Execution':
            return Token(EXECUTION, result)
        elif result == 'INT':
            return Token(TYPE, result)
        elif result == 'STRING':
            return Token(TYPE, result)
        elif result == 'FLOAT':
            return Token(TYPE, result)
        elif result == 'ARRAY':
            return Token(TYPE, result)
        elif result == 'BOOL':
            return Token(TYPE, result)
        elif result == 'VOID':
            return Token(TYPE, result)
        elif result == 'AND':
            return Token(AND, 'and')
        elif result == 'OR':
            return Token(OR, 'or')
        elif result == 'NOT':
            return Token(NOT, 'not')
        elif result == 'DIV':
            return Token(DIV, '//')
        elif result == 'MOD':
            return Token(MOD, '%')
        elif result == 'COND':
            return Token(COND, result)
        elif result == 'LOOP':
            return Token(LOOP, result)
        elif result == 'RETURN':
            return Token(RETURN, 'return')
        else:
            return Token(ID, result)

    def string(self):
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char != '\'':
            result += self.current_char
            self.advance()

        self.advance()
        return Token(STRING, result)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line_count += 1
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()

            if self.current_char is None:
                return Token(EOF, None)

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == '-':
                self.advance()
                if self.current_char == '>':
                    self.advance()
                    return Token(ARROW, '->')
                else:
                    return Token(MINUS, '-')

            if self.current_char == '\'':
                return self.string()

            if self.current_char == '#':
                result = '#'
                self.advance()
                if self.current_char.isalpha():
                    result += self._id().value
                return Token(ID, result)

            if self.current_char == '@':
                self.advance()
                return Token(MONKEY, '@')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == ';':
                self.advance()
                return Token(SEMICOLON, ';')

            if self.current_char == '{':
                self.advance()
                return Token(LBRACKET, '{')

            if self.current_char == '}':
                self.advance()
                return Token(RBRACKET, '}')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            if self.current_char == '#':
                self.advance()
                return Token(HASH, '#')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(NDIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(LESS_EQ, '<=')
                return Token(LESS, '<')

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(GREATER_EQ, '>=')
                return Token(GREATER, '>')

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(EQUAL, '==')
                return Token(ASSIGN, '=')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(NOT_EQUAL, '!=')
                self.error()

            self.error()

        return Token(EOF, None)
