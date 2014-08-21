#!/usr/bin/env python
import sys

def chunk_name(name):
    r = []
    w = ''
    u0 = False
    for c in name:
        if c.isalpha():
            u1 = c.isupper()
            if not u0 and u1:
                if w:
                    r.append(w); w = ''
            elif u0 and not u1:
                if 2 <= len(w):
                    r.append(w[:-1])
                    w = w[-1:]
            w += c
            u0 = u1
        else:
            if w:
                r.append(w); w = ''
            u0 = False
    if w:
        r.append(w)
    return [ w.lower() for w in r if 2 <= len(w) ]

assert chunk_name('thisisaword') == ['thisisaword']
assert chunk_name('this_is_a_word') == ['this','is','word']
assert chunk_name('WHOAREU') == ['whoareu']
assert chunk_name('WHO_ARE_U') == ['who','are']
assert chunk_name('XMLIsDerpy') == ['xml','is','derpy']
assert chunk_name('fancyURLOpener') == ['fancy','url','opener']

def count(d, k):
    assert k
    if k not in d:
        d[k] = 1
    else:
        d[k] += 1
    return

def dump(d, n=100):
    for (k,v) in sorted(d.iteritems(), key=lambda (k,v):v, reverse=True):
        if isinstance(k, basestring):
            print ' ', v, k
        else:
            print ' ', v, ' '.join(k)
        n -= 1
        if n == 0: break
    print
    return

class Stat(object):

    def __init__(self, name):
        self.name = name
        self.word = {}
        self.prefix = {}
        self.suffix = {}
        self.bigram = {}
        return

    def add(self, v):
        words = chunk_name(v)
        if not words: return
        for w in words:
            count(self.word, w)
        if 2 <= len(words):
            count(self.prefix, words[0])
            count(self.suffix, words[-1])
        for (w1,w2) in zip(words[:-1], words[1:]):
            count(self.bigram, (w1,w2))
        return

    def show(self, n=100):
        print '+%s_word:' % self.name
        dump(self.word, n=n)
        print '+%s_prefix:' % self.name
        dump(self.prefix, n=n)
        print '+%s_suffix:' % self.name
        dump(self.suffix, n=n)
        print '+%s_bigram:' % self.name
        dump(self.bigram, n=n)
        return


def main(argv):
    import fileinput
    
    varstat = Stat('var')
    typestat = Stat('type')
    funcstat = Stat('func')
    func_verb = {}
    func_assoc = {}
    for line in fileinput.input():
        (k,_,v) = line.strip().partition(' ')
        if k == 'vardecl':
            varstat.add(v)
        elif k == 'typedecl':
            typestat.add(v)
        elif k == 'funcdecl' or k == 'funcall':
            (name,_,args) = v.partition(' ')
            funcstat.add(name)
            words = chunk_name(name)
            if 2 <= len(words):
                verbs = (words[0], words[-1])
            elif words:
                verbs = (words[-1],)
            else:
                continue
            nouns = []
            for noun in args.split(' '):
                varstat.add(noun)
                words = chunk_name(noun)
                if words:
                    nouns.append(words[-1])
            for v in verbs:
                for n in nouns:
                    count(func_verb, (v,n))
            for (i,n1) in enumerate(nouns):
                for n2 in nouns[i+1:]:
                    if n1 == n2: continue
                    k = ( (n1,n2) if n1 < n2 else (n2,n1) )
                    count(func_assoc, k)
    #
    n = 100
    varstat.show(n=n)
    typestat.show(n=n)
    funcstat.show(n=n)
    print '+func_verb:'
    dump(func_verb, n=n)
    print '+func_assoc:'
    dump(func_assoc, n=n)
    return

if __name__ == '__main__': sys.exit(main(sys.argv))
