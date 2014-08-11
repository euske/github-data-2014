#!/usr/bin/env python

class SexprParser(object):

    def __init__(self):
        self._stack = []
        self._expr = []
        self._parse = self._parse_main
        return

    def feed(self, s):
        i = 0
        while i < len(s):
            i = self._parse(s, i)
        return

    def get(self):
        assert len(self._expr) == 1
        return self._expr.pop()

    def _parse_main(self, s, i):
        c = s[i]
        if c == '(':
            self._parse = self._parse_paren0
            return i+1
        elif c == ')':
            assert self._stack
            self._stack[-1].append(self._expr)
            self._expr = self._stack.pop()
            return i+1
        elif c == ' ':
            self._parse = self._parse_space
            return i+1
        elif c == '"':
            self._string = ''
            self._parse = self._parse_string
            return i+1
        else:
            self._symbol = c
            self._parse = self._parse_symbol
            return i+1

    def _parse_paren0(self, s, i):
        c = s[i]
        if c == ' ':
            self._symbol = '('
            self._expr.append('.'+self._symbol)
            self._parse = self._parse_main
            return i+1
        else:
            self._stack.append(self._expr)
            self._expr = []
            self._parse = self._parse_main
            return i

    def _parse_space(self, s, i):
        c = s[i]
        if c == ')':
            self._symbol = ')'
            self._expr.append('.'+self._symbol)
            self._parse = self._parse_main
            return i+1
        else:
            self._parse = self._parse_main
            return i

    def _parse_symbol(self, s, i):
        c = s[i]
        if c == ')':
            self._expr.append('.'+self._symbol)
            self._parse = self._parse_main
            return i
        elif c == ' ':
            self._expr.append('.'+self._symbol)
            self._parse = self._parse_main
            return i+1
        else:
            self._symbol += c
            return i+1
    
    def _parse_string(self, s, i):
        c = s[i]
        if c == '"':
            self._expr.append('@'+self._string)
            self._parse = self._parse_main
            return i+1
        elif c == '\\':
            self._parse = self._parse_string_b
            return i+1
        else:
            self._string += c
            return i+1

    def _parse_string_b(self, s, i):
        c = s[i]
        self._string += c
        self._parse = self._parse_string
        return i+1
