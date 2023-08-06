#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .errors import GitQLError
from .token import TokenType, Token
from .ast import (NumNode, StringNode, IdentifierNode, UnaryOpNode, BinOpNode,
                  WhereNode, OrderNode, LimitNode, SelectNode)


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def error(self, expect):
        message = 'Got {!r} while expect {!r}.'.format(
            self.current_token.token_type.name, expect.name)
        raise GitQLError(message)

    def eat(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    def term_unary(self, precedence, token_types):
        term_fn1 = getattr(self, 'term' + str(precedence))
        term_fn2 = getattr(self, 'term' + str(precedence - 1))

        if self.current_token.token_type not in token_types:
            node = term_fn2()
        else:
            token = self.current_token

            self.eat(token.token_type)

            node = UnaryOpNode(term_fn1(), token)

        return node

    def term_binary(self, precedence, token_types):
        term_fn = getattr(self, 'term' + str(precedence - 1))

        node = term_fn()

        while self.current_token.token_type in token_types:
            token = self.current_token

            self.eat(token.token_type)

            node = BinOpNode(node, token, term_fn())

        return node

    def term0(self):
        token = self.current_token
        if token.token_type == TokenType.T_NUMBER:
            self.eat(TokenType.T_NUMBER)
            return NumNode(token)
        elif token.token_type == TokenType.T_STRING:
            self.eat(TokenType.T_STRING)
            return StringNode(token)
        elif token.token_type == TokenType.T_LPARAN:
            self.eat(TokenType.T_LPARAN)
            node = self.expr()
            self.eat(TokenType.T_RPARAN)
            return node
        else:
            return self.identifer()

    def term1(self):
        token_types = (TokenType.T_IN, TokenType.T_EQ, TokenType.T_LT,
                       TokenType.T_LTE, TokenType.T_GT, TokenType.T_GTE)
        return self.term_binary(1, token_types)

    def term2(self):
        return self.term_unary(2, (TokenType.T_NOT, ))

    def term3(self):
        return self.term_binary(3, (TokenType.T_AND, TokenType.T_OR))

    def expr(self):
        return self.term3()

    def identifer(self):
        node = IdentifierNode(self.current_token)
        self.eat(TokenType.T_IDENTIFIER)
        return node

    def field(self):
        if self.current_token.token_type == TokenType.T_ASTERISK:
            token = self.current_token
            self.eat(TokenType.T_ASTERISK)
            return IdentifierNode(token)
        return self.identifer()

    def fields(self):
        nodes = [self.field()]

        while (self.current_token.token_type != TokenType.T_EOF and
               self.current_token.token_type == TokenType.T_COMMA):
            self.eat(TokenType.T_COMMA)
            nodes.append(self.field())

        return nodes

    def table(self):
        return self.identifer()

    def where(self):
        if self.current_token.token_type != TokenType.T_WHERE:
            return None

        self.eat(TokenType.T_WHERE)
        return WhereNode(self.expr())

    def order(self):
        if self.current_token.token_type != TokenType.T_ORDER:
            return None

        self.eat(TokenType.T_ORDER)
        self.eat(TokenType.T_BY)

        field = self.identifer()

        order_token = self.current_token
        if order_token.token_type not in (TokenType.T_ASC, TokenType.T_DESC):
            order_token = Token(TokenType.T_ASC, 'ASC')
        else:
            self.eat(order_token.token_type)
        return OrderNode(field, order_token)

    def limit(self):
        if self.current_token.token_type != TokenType.T_LIMIT:
            # Default limit
            return LimitNode()

        self.eat(TokenType.T_LIMIT)

        limit_token = self.current_token
        self.eat(TokenType.T_NUMBER)

        token = self.current_token
        if token.token_type in (TokenType.T_COMMA, TokenType.T_OFFSET):
            self.eat(token.token_type)
            offset_token = self.current_token
            self.eat(TokenType.T_NUMBER)
            return LimitNode(limit_token, offset_token)
        else:
            return LimitNode(limit_token)

    def select(self):
        self.eat(TokenType.T_SELECT)
        fields = self.fields()
        self.eat(TokenType.T_FROM)
        table = self.table()
        where = self.where()
        order = self.order()
        limit = self.limit()

        if self.current_token.token_type == TokenType.T_SEMICOLON:
            self.eat(TokenType.T_SEMICOLON)

        return SelectNode(fields, table, where, order, limit)

    def parse(self):
        self.current_token = self.lexer.get_next_token()

        node = self.select()

        if self.current_token.token_type != TokenType.T_EOF:
            self.error(TokenType.T_EOF)

        return node
