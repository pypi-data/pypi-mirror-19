#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

from . import red
from .errors import GitQLError
from .token import TokenType, Token


class Lexer(object):
    # All keywords reversed.
    REVERSED_KEYWORDS = {
        'select': TokenType.T_SELECT,
        'from': TokenType.T_FROM,
        'where': TokenType.T_WHERE,
        'order': TokenType.T_ORDER,
        'by': TokenType.T_BY,
        'limit': TokenType.T_LIMIT,
        'offset': TokenType.T_OFFSET,
        'in': TokenType.T_IN,
        'desc': TokenType.T_DESC,
        'asc': TokenType.T_ASC,
        'and': TokenType.T_AND,
        'or': TokenType.T_OR,
        'not': TokenType.T_NOT,
    }

    # Token types which needs only single character.
    SINGLE_CHAR_TYPES = {
        '*': TokenType.T_ASTERISK,
        ',': TokenType.T_COMMA,
        ';': TokenType.T_SEMICOLON,
        '(': TokenType.T_LPARAN,
        ')': TokenType.T_RPARAN,
        '=': TokenType.T_EQ,
    }

    # Token types which may have two characters.
    TWO_CHAR_TYPES = {
        # The value is:
        # second character,
        # token type when single character,
        # token type when double character
        '>': ('=', TokenType.T_GT, TokenType.T_GTE),
        '<': ('=', TokenType.T_LT, TokenType.T_LTE),
    }

    def __init__(self, s=''):
        self.rewind(s)

    def rewind(self, s=''):
        self.source = s
        self.source_len = len(s)
        self.pos = 0
        self.current_char = self.source[self.pos] if self.source_len else None

    def error(self):
        print('\t{}'.format(red(self.source)))
        print('\t{}^'.format(' ' * self.pos))
        raise GitQLError('invalid character')

    def eof(self, pos=None):
        if pos is None:
            pos = self.pos
        return pos > self.source_len - 1

    def skip_whitespaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        s = ''

        if self.current_char == '-':
            s += '-'
            self.advance()
            if not self.current_char.isdigit():
                self.error()

        while self.current_char is not None and self.current_char.isdigit():
            s += self.current_char
            self.advance()

        return Token(TokenType.T_NUMBER, int(s))

    def string(self):
        s = ''
        delimeter = self.current_char

        # Eat the left delimeter
        self.advance()

        while self.current_char is not None and self.current_char != delimeter:
            if self.current_char == '\\':
                self.advance()
            s += self.current_char
            self.advance()

        if self.current_char != delimeter:
            self.error()

        # Eat the right delimeter
        self.advance()

        return Token(TokenType.T_STRING, s)

    def identifier(self):
        s = ''
        valid_chars = string.ascii_letters + '_'

        while (self.current_char is not None and
               self.current_char in valid_chars):
            s += self.current_char
            self.advance()

        token_type = self.REVERSED_KEYWORDS.get(s.lower(),
                                                TokenType.T_IDENTIFIER)
        return Token(token_type, s)

    def peek(self):
        pos = self.pos + 1

        if self.eof(pos):
            return None
        else:
            return self.source[pos]

    def advance(self):
        self.pos += 1

        if self.eof():
            self.current_char = None
        else:
            self.current_char = self.source[self.pos]

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespaces()
                continue
            elif self.current_char == '-' or self.current_char.isdigit():
                return self.integer()
            elif self.current_char in ('\'', '"'):
                return self.string()
            elif self.current_char.isalpha():
                return self.identifier()
            elif self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.T_NEQ, '!=')
                else:
                    self.error()
            elif self.current_char in self.SINGLE_CHAR_TYPES:
                c = self.current_char
                self.advance()
                return Token(self.SINGLE_CHAR_TYPES[c], c)
            elif self.current_char in self.TWO_CHAR_TYPES:
                c = self.current_char
                second_c, single_dt, double_dt = self.TWO_CHAR_TYPES[c]
                if self.peek() == second_c:
                    self.advance()
                    self.advance()
                    return Token(double_dt, c + second_c)
                else:
                    self.advance()
                    return Token(single_dt, c)
            else:
                self.error()

        return Token(TokenType.T_EOF, None)
