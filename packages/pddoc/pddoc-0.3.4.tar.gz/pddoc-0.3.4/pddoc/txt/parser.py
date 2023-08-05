#!/usr/bin/env python
# coding=utf-8

#   Copyright (C) 2016 by Serge Poltavski                                 #
#   serge.poltavski@gmail.com                                             #
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 3 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
#   This program is distributed in the hope that it will be useful,       #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#   GNU General Public License for more details.                          #
#                                                                         #
#   You should have received a copy of the GNU General Public License     #
#   along with this program. If not, see <http://www.gnu.org/licenses/>   #

from __future__ import print_function
from itertools import ifilter
import graph_lexer as lex
import re
from pddoc.pd import Message, Comment, Canvas
from six import string_types
from pddoc.pd import factory
from pddoc.pd.coregui import CoreGui
import copy
import logging


class Node(object):
    def __init__(self, tok, char_pos):
        self.tok = tok
        self.char_pos_ = char_pos
        self.pd_object = None
        self.conn_src_id = None
        self.conn_src_outlet = 0
        self.conn_dest_id = None
        self.conn_dest_inlet = 0
        self.connected = False
        self.obj_line_index = -1

        if self.tok and self.is_connection():
            # calc connection source outlet
            self.conn_src_outlet = self.tok.value.count('^')
            self.conn_dest_inlet = self.tok.value.count('.')

            # only single \
            if self.tok.value == '\\':
                self.conn_dest_inlet += 1

    def group(self, n=1):
        return self.tok.lexmatch.group(n)

    def is_object(self):
        if self.tok is None:
            return False

        return self.tok.type in ('OBJECT', 'MESSAGE', 'COMMENT')

    def is_connection(self):
        return self.tok.type in ('CONNECTION', 'CONNECTION_LEFT', 'CONNECTION_RIGHT', 'CONNECTION_X')

    @property
    def id(self):
        return self.line_pos * 1000 + self.char_pos

    @property
    def type(self):
        if self.tok is None:
            return None

        return self.tok.type

    @property
    def width(self):
        return len(self.tok.value)

    @property
    def value(self):
        return self.tok.value

    @property
    def line_pos(self):
        return self.tok.lineno - 1

    @property
    def char_pos(self):
        return self.char_pos_

    def contains(self, char_pos):
        return self.char_pos <= char_pos <= (self.char_pos + self.width)


class Parser(object):
    X_PAD = 20
    Y_PAD = 20
    X_SPACE = 8
    Y_SPACE = 12

    ALIASES = {
        '_': 'tgl',
        'T': 'tgl',
        'B': 'bng',
        'O': 'bng',
        'o': 'bng',
        'fa': 'floatatom',
        'F': 'floatatom',
        'S': 'symbolatom'
    }

    def __init__(self):
        self.lines = []
        self.lines_len = []
        self.tokens = []
        self.nodes = []
        self.lexer = lex.lexer()

    def clear(self):
        self.lines = []
        self.lines_len = []
        self.tokens = []
        self.nodes = []
        self.lexer = lex.lexer()

    def parse_file(self, fname):
        with open(fname) as f:
            self.parse(f.read())

    def node_by_id(self, id):
        res = filter(lambda n: id == n.id, self.nodes)
        if len(res) < 1:
            return None

        return res[0]

    def parse(self, string):
        assert isinstance(string, string_types)

        self.lines = string.split('\n')
        self.lines_len = map(lambda x: len(x), self.lines)
        self.lexer.input(string)
        self.parse_tokens()
        self.parse_nodes()
        self.enumerate_objects()
        self.parse_connections()
        self.layout_nodes()
        return True

    def token_line_lex_pos(self, lexline, lexpos):
        assert lexpos >= 0
        assert lexline >= 0
        assert lexline < len(self.lines_len)

        return lexpos - sum(self.lines_len[0:lexline]) - lexline

    def enumerate_objects(self):
        for l in range(0, self.num_lines()):
            idx = 0
            for o in filter(lambda x: x.line_pos == l, self.nodes):
                o.obj_line_index = idx
                idx += 1

    def parse_tokens(self):
        while True:
            tok = self.lexer.token()
            if not tok:
                break

            self.tokens.append(tok)

            ln = tok.lineno - 1
            char_pos = self.token_line_lex_pos(ln, tok.lexpos)
            n = Node(tok, char_pos)
            self.nodes.append(n)

    @classmethod
    def find_alias(cls, atoms):
        name = atoms[0]
        args = atoms[1:]
        if name in cls.ALIASES:
            return cls.ALIASES[name], args
        return name, args

    def parse_nodes(self):
        for n in filter(lambda x: x.is_object(), self.nodes):
            if n.type == 'OBJECT':
                m = re.match(lex.r_OBJECT, n.value)
                # filter spaces and #ID values
                atoms = filter(lambda a: len(a) > 0 and (not a.startswith('#')), m.group(1).split(' '))
                assert len(atoms) > 0
                name, args = self.find_alias(atoms)
                if CoreGui.is_coregui(name):
                    kwargs = dict(map(lambda x: tuple(x.split('=')), args))
                    n.pd_object = factory.make_by_name(name, **kwargs)
                elif name == 'pd':
                    n.pd_object = Canvas.subpatch(args[0])
                else:
                    n.pd_object = factory.make_by_name(name, args)
            elif n.type == 'MESSAGE':
                m = re.match(lex.r_MESSAGE, n.value)
                txt = m.group(1).replace(',', '\,')
                # logging.warning(txt)
                args = txt.split(' ')
                n.pd_object = Message(0, 0, args)
            elif n.type == 'COMMENT':
                m = re.match(lex.r_COMMENT, n.value)
                txt = m.group(1).replace(';', ' \;').replace(',', ' \,')
                n.pd_object = Comment(0, 0, txt.split(' '))
            else:
                logging.warning("Unknown type {0:s}".format(n.type))

    def parse_connections(self):
        for c in filter(lambda n: n.is_connection(), self.nodes):
            self.process_connection(c)

    def find_connection(self, line, char_pos):
        """
        :type line: int
        :type char_pos: list
        """
        return next(ifilter(
            lambda x:
            x.line_pos == line and any(map(lambda c: x.contains(c), char_pos)), self.nodes), None)

    def find_by_line_idx(self, line, idx):
        return next((ifilter(lambda n: n.line_pos == line and n.obj_line_index == idx, self.nodes)), None)

    def process_cross_connection(self, conn):
        assert isinstance(conn, Node)
        line = conn.line_pos
        src_idx = conn.obj_line_index - 1
        dest_idx = conn.obj_line_index + 1

        src = self.find_by_line_idx(line, src_idx)
        dest = self.find_by_line_idx(line, dest_idx)

        if src and dest:
            c1 = copy.deepcopy(conn)
            c1.tok.type = 'CONNECTION'
            c1.conn_src_id = src.id
            c1.conn_dest_id = dest.id
            c1.conn_dest_inlet = 0
            c1.conn_src_outlet = len(src.pd_object.outlets()) - 1
            c1.connected = True

            c2 = copy.deepcopy(conn)
            c2.tok.type = 'CONNECTION'
            c2.conn_src_id = dest.id
            c2.conn_dest_id = src.id
            c2.conn_src_outlet = 0
            c2.conn_dest_inlet = len(src.pd_object.inlets()) - 1
            c2.connected = True

            self.nodes.append(c1)
            self.nodes.append(c2)

    def process_connection(self, c):
        if c.type == 'CONNECTION_X':
            self.process_cross_connection(c)
            return

        conn_start = []
        if c.type == 'CONNECTION_LEFT':
            conn_start = [c.char_pos + c.tok.value.index('/')]
        else:
            conn_start = [c.char_pos]

        # find object on previous line
        src = self.find_connection(c.line_pos - 1, conn_start)
        if src is None:
            print("connection source is not found for: {0:s}".format(c))
            return

        c.conn_src_id = src.id
        if src.is_connection():
            # multiline connection
            c.conn_src_id = src.conn_src_id
            c.conn_src_outlet = src.conn_src_outlet
            src.connected = False

        # find on next line
        dest = self.find_connection(c.line_pos + 1, [c.char_pos, c.char_pos + c.width])
        if dest is None:
            print("connection destination is not found for: {0:s}".format(c.tok.value))
            return

        c.conn_dest_id = dest.id
        c.connected = True

    def layout_nodes(self):
        obj = filter(lambda x: x.is_object(), self.nodes)
        for n in obj:
            n.pd_object.x = n.char_pos * self.X_SPACE + self.X_PAD
            n.pd_object.y = n.line_pos * self.Y_SPACE + self.Y_PAD

    def num_lines(self):
        return len(self.lines)

    def num_elements(self, type):
        return len(self.elements(type))

    def elements(self, type):
        return filter(lambda x: x.type == type, self.nodes)

    def elements_in_line(self, type, line_pos):
        return filter(lambda x: x.type == type and x.line_pos == line_pos, self.nodes)

    def export(self, cnv):
        assert isinstance(cnv, Canvas)
        for n in filter(lambda x: x.is_object(), self.nodes):
            cnv.append_object(n.pd_object)

        for c in filter(lambda x: x.is_connection() and x.connected, self.nodes):
            # print("connection %s -> %s" % (c.conn_src_id, c.conn_dest_id))
            src = self.node_by_id(c.conn_src_id)
            dest = self.node_by_id(c.conn_dest_id)

            if src and dest:
                # print("add connection: {0:d}-> {1:d}".format(src.pd_object.id, dest.pd_object.id))
                cnv.add_connection(
                    src.pd_object.id,
                    c.conn_src_outlet,
                    dest.pd_object.id,
                    c.conn_dest_inlet)
