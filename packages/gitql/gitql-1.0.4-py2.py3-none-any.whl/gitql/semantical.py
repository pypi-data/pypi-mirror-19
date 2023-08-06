#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections

from . import PossibleTables, get_possible_fields
from .token import TokenType
from .ast import NumNode, StringNode, IdentifierNode
from .visitor import NodeVisitor


class SemanticalChecker(NodeVisitor):
    def check_table(self, node):
        table = node.table.value
        if table.lower() not in PossibleTables:
            return 'Table {!r} not found'.format(table)

    def check_fields(self, node):
        # Duplication
        ct = collections.Counter(f.value.lower() for f in node.fields)
        mc = ct.most_common(1)[0]
        if mc[1] > 1:
            return 'Field {!r} found many times.'.format(mc[0])

        # Existance
        table = node.table.value
        possible_fields = get_possible_fields(table)
        for field in ct:
            if field != '*' and field not in possible_fields:
                return 'Field {!r} not found in Table {!r}'.format(field,
                                                                   table)

    def visit_num(self, node):
        pass

    def visit_string(self, node):
        pass

    def visit_identifier(self, node):
        pass

    def visit_unaryop(self, node):
        token_type = node.op.token_type
        if token_type == TokenType.T_NOT:
            return self.visit(node.expr)
        else:
            # What's wrong...
            pass

    def visit_binop(self, node):
        token_type = node.op.token_type
        if token_type in (TokenType.T_AND, TokenType.T_OR):
            return self.visit(node.left) or self.visit(node.right)
        elif token_type in (TokenType.T_NEQ, TokenType.T_EQ, TokenType.T_IN,
                            TokenType.T_LT, TokenType.T_LTE, TokenType.T_GT,
                            TokenType.T_GTE):
            valid_classes = (NumNode, StringNode, IdentifierNode)
            if (not isinstance(node.left, valid_classes) or
                    not isinstance(node.right, valid_classes)):
                return 'unsupport expression in where condition.'
        else:
            # What's wrong...
            pass

    def check_where(self, node):
        return node.where and self.visit(node.where.cond)

    def check_order(self, node):
        if not node.order:
            return

        table = node.table.value
        possible_fields = get_possible_fields(table)
        field = node.order.field.value
        if field.lower() not in possible_fields:
            return 'Field {!r} of Order not found in Table {!r}'.format(field,
                                                                        table)

    def check_limit(self, node):
        if node.limit.limit.value < -1:
            return "Limit can't less than -1."
        if node.limit.offset.value < 0:
            return "Offset of limit can't less than 0."

    def analysis(self, node):
        checkers = (self.check_table, self.check_fields, self.check_where,
                    self.check_order, self.check_limit)
        for check in checkers:
            err_msg = check(node)
            if err_msg:
                return True, err_msg
        return False, None
