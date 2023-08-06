#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .token import TokenType, Token


class AST(object):
    """Base class of Abstract-Syntax-Tree. """
    pass


class NumNode(AST):
    """Number node."""

    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return '{!r}'.foramt(self.value)


class StringNode(AST):
    """String node."""

    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return '{!r}'.format(self.value)


class IdentifierNode(AST):
    """Identifier node."""

    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return '{!r}'.format(self.value)


class UnaryOpNode(AST):
    """Unary operator node."""

    def __init__(self, expr, op):
        self.expr = expr
        self.token = self.op = op

    def __repr__(self):
        return '{!r}: ({!r})'.format(self.op.value, self.expr)


class BinOpNode(AST):
    """Binary operator node."""

    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self):
        return '({!r} {!r} {!r})'.format(self.left, self.op.value, self.right)


class WhereNode(AST):
    """Where clauses node."""

    def __init__(self, cond):
        self.cond = cond

    def __repr__(self):
        return '{!r}'.format(self.cond)


class OrderNode(AST):
    """Order by node."""

    def __init__(self, field, order):
        self.field = field
        self.token = self.order = order
        self.asc = self.token.token_type == TokenType.T_ASC

    def __repr__(self):
        return '{!r} {!r}'.format(self.field, self.asc)


class LimitNode(AST):
    """Limit node."""

    def __init__(self,
                 limit=Token(TokenType.T_NUMBER, 10),
                 offset=Token(TokenType.T_NUMBER, 0)):
        self.limit = limit
        self.offset = offset

    def __repr__(self):
        return '{!r} {!r}'.format(self.limit.value, self.offset.value)


class SelectNode(AST):
    """Select statement node."""

    def __init__(self, fields, table, where, order, limit):
        self.fields = fields
        self.table = table
        self.where = where
        self.order = order
        self.limit = limit
