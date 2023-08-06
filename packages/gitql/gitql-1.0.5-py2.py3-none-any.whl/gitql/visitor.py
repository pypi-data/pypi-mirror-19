#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .errors import GitQLError


class NodeVisitor(object):
    @staticmethod
    def get_method_name(node):
        name = type(node).__name__.lower()  # lower() make PEP happy.
        if name.endswith('node'):
            name = name[:-4]
        return 'visit_' + name

    def visit(self, node):
        name = self.get_method_name(node)
        visit_fn = getattr(self, name, self.visit_unknown)
        return visit_fn(node)

    def visit_unknown(self, node):
        name = self.get_method_name(node)
        raise GitQLError('No {} method.'.format(name))
