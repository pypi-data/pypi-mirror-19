#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter

import git

from . import get_possible_fields
from .errors import GitQLError
from .token import TokenType, Token
from .ast import IdentifierNode
from .visitor import NodeVisitor
from .semantical import SemanticalChecker


class GitQL(NodeVisitor):
    def __init__(self, parser, path):
        try:
            self.repo = git.Repo(path)
        except (git.exc.InvalidGitRepositoryError,
                git.exc.NoSuchPathError) as e:
            raise GitQLError("'{}' is not a valid git repository".format(e))

        self.parser = parser
        self.row_data = None

    def git_ref_types(self, ref):
        if isinstance(ref, git.RemoteReference):
            return 'remote'
        elif isinstance(ref, git.Head):
            return 'branch'
        elif isinstance(ref, git.TagReference):
            return 'tag'
        else:
            return ''

    def update_row_data(self, obj):
        if isinstance(obj, git.Commit):
            data = {
                'author': obj.author.name,
                'author_email': obj.author.email,
                'committer': obj.committer.name,
                'committer_email': obj.committer.email,
                'hash': obj.hexsha,
                'date': obj.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'summary': obj.summary,
                'message': obj.message
            }
        elif isinstance(obj, git.Remote):
            data = {
                'name': obj.name,
                'url': obj.repo.git.remote('get-url', obj.name),
                'push_url': obj.repo.git.remote('get-url', '--push', obj.name),
                'owner': obj.repo.git_dir
            }
        elif isinstance(obj, (git.Head, git.RemoteReference,
                              git.TagReference)):
            data = {
                'name': obj.name,
                'full_name': obj.to_full_path(obj.name),
                'hash': obj.object.hexsha,
                'type': self.git_ref_types(obj)
            }
        else:
            data = {}

        self.row_data = data

    def walk(self, node, objects):
        limit = node.limit.limit.value
        offset = node.limit.offset.value
        n = 0
        rows = []

        header = [field.value for field in node.fields]
        header_lower = [field.lower() for field in header]

        for obj in objects:
            if limit != -1 and n >= limit:
                break

            self.update_row_data(obj)

            if node.where and not self.visit(node.where.cond):
                continue

            if offset:
                offset -= 1
                continue

            n += 1
            row = [self.row_data[field] for field in header_lower]
            rows.append(row)

        if node.order:
            i = header_lower.index(node.order.field.value.lower())
            rows.sort(key=itemgetter(i), reverse=not node.order.asc)

        return header, rows

    def walkCommits(self, node):
        return self.walk(node, self.repo.iter_commits())

    def walkRemotes(self, node):
        return self.walk(node, self.repo.remotes)

    def walkTags(self, node):
        return self.walk(node, self.repo.tags)

    def walkBranches(self, node):
        return self.walk(node, self.repo.branches)

    def walkRefs(self, node):
        return self.walk(node, self.repo.refs)

    def visit_num(self, node):
        return node.value

    def visit_string(self, node):
        return node.value

    def visit_identifier(self, node):
        return self.row_data[node.value.lower()]

    def visit_unaryop(self, node):
        token_type = node.op.token_type
        if token_type == TokenType.T_NOT:
            return not self.visit(node.expr)
        else:
            # What's wrong...
            pass

    def visit_binop(self, node):
        op_funcs = {
            TokenType.T_AND: lambda x, y: x and y,
            TokenType.T_OR: lambda x, y: x or y,
            TokenType.T_EQ: lambda x, y: x == y,
            TokenType.T_NEQ: lambda x, y: x != y,
            TokenType.T_LT: lambda x, y: x < y,
            TokenType.T_LTE: lambda x, y: x <= y,
            TokenType.T_GT: lambda x, y: x > y,
            TokenType.T_GTE: lambda x, y: x >= y,
            TokenType.T_IN: lambda x, y: x in y
        }

        return op_funcs[node.op.token_type](self.visit(node.left),
                                            self.visit(node.right))

    def expandAsterisk(self, node):
        table = node.table.value
        possible_field_nodes = [
            IdentifierNode(Token(TokenType.T_IDENTIFIER, f))
            for f in get_possible_fields(table)
        ]
        for i, field in enumerate(node.fields):
            if field.token.token_type == TokenType.T_ASTERISK:
                node.fields[i:i + 1] = possible_field_nodes
                return

    def visit_select(self, node):
        self.expandAsterisk(node)

        walkers = {
            'commits': self.walkCommits,
            'remotes': self.walkRemotes,
            'tags': self.walkTags,
            'branches': self.walkBranches,
            'refs': self.walkRefs
        }
        return walkers[node.table.value.lower()](node)

    def run(self):
        node = self.parser.parse()

        checker = SemanticalChecker()
        err, msg = checker.analysis(node)
        if err:
            raise GitQLError(msg)

        return self.visit(node)
