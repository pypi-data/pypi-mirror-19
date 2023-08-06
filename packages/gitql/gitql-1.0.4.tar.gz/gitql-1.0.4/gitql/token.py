#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

# Borrow from Lib/enum.py
_auto_null = object()


class auto:
    """
    Instances are replaced with an appropriate value in Enum class suites.
    """
    value = _auto_null


class TokenType(Enum):
    T_SELECT = auto()
    T_FROM = auto()
    T_WHERE = auto()
    T_ORDER = auto()
    T_BY = auto()
    T_LIMIT = auto()
    T_OFFSET = auto()
    T_IN = auto()
    T_DESC = auto()
    T_ASC = auto()
    T_AND = auto()
    T_OR = auto()
    T_NOT = auto()
    T_IDENTIFIER = auto()
    T_NUMBER = auto()
    T_STRING = auto()
    T_ASTERISK = auto()  # *
    T_COMMA = auto()  # ,
    T_SEMICOLON = auto()  # ;
    T_LPARAN = auto()  # auto(
    T_RPARAN = auto()  # )
    T_EQ = auto()  # =
    T_GT = auto()  # >
    T_GTE = auto()  # >=
    T_LT = auto()  # <
    T_LTE = auto()  # <=
    T_NEQ = auto()  # !=
    T_EOF = auto()


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return 'Token({!r}, {!r})'.format(self.token_type.name, self.value)
