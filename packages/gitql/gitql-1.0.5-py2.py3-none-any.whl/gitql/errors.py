#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import red


class GitQLError(Exception):
    """Exceptions in gitql."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return '{}: {}'.format(red('GitQLError'), self.message)
