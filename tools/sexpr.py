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
            #print i, s[i], self._parse
            i = self._parse(s[i], i)
        return

    def close(self):
        #assert not self._stack, self._stack
        return self._expr

    def get(self):
        assert len(self._expr)
        return self._expr.pop()

    def _add_symbol(self, symbol):
        #print 'add', symbol
        self._expr.append('.'+symbol)
        return

    def _parse_main(self, c, i):
        if c == '(':
            self._stack.append(self._expr)
            #print 'open', len(self._stack)
            self._expr = []
            return i+1
        elif c == ')':
            assert self._stack
            self._stack[-1].append(self._expr)
            self._expr = self._stack.pop()
            #print 'close', len(self._stack)
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

    def _parse_space(self, c, i):
        if c == '(':
            self._parse = self._parse_paren0
            return i+1
        elif c == ')':
            self._add_symbol(')')
            self._parse = self._parse_main
            return i+1
        else:
            self._parse = self._parse_main
            return i

    def _parse_paren0(self, c, i):
        if c == ' ':
            self._add_symbol('(')
            self._parse = self._parse_space
            return i+1
        else:
            self._stack.append(self._expr)
            #print 'open', len(self._stack)
            self._expr = []
            self._parse = self._parse_main
            return i

    def _parse_symbol(self, c, i):
        if c == ')':
            self._add_symbol(self._symbol)
            self._parse = self._parse_main
            return i
        elif c == ' ':
            self._add_symbol(self._symbol)
            self._parse = self._parse_space
            return i+1
        else:
            self._symbol += c
            return i+1
    
    def _parse_string(self, c, i):
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

    def _parse_string_b(self, c, i):
        self._string += c
        self._parse = self._parse_string
        return i+1

if __name__ == '__main__':
    import fileinput
    parser = SexprParser()
    for line in fileinput.input():
        parser.feed(line.strip())
    print parser.close()
