#!/usr/bin/env python
# -*- coding: utf-8 -*-

from termcolor import colored

__version__ = '1.0.5'

# Supported tables and fields.
PossibleTables = {
    'commits': [
        'hash',
        'date',
        'author',
        'author_email',
        'committer',
        'committer_email',
        'summary',
        'message',
    ],
    'refs': [
        'name',
        'full_name',
        'type',
        'hash',
    ],
    'remotes': [
        'name',
        'url',
        'push_url',
        'owner',
    ],
    'tags': [
        'name',
        'full_name',
        'hash',
    ],
    'branches': [
        'name',
        'full_name',
        'hash',
    ],
}


def get_possible_fields(table):
    return PossibleTables.get(table.lower(), [])


def show_all_tables():
    print('Tables: \n')
    for table, fields in PossibleTables.items():
        print('{}'.format(table))
        print('\t{}.\n'.format(', '.join(fields)))


def red(s):
    return colored(s, 'red')


def bold(s):
    return colored(s, attrs=['bold'])
