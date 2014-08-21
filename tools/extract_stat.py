#!/usr/bin/env python
# makestat.py
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
    return r

assert chunk_name('thisisaword') == ['thisisaword']
assert chunk_name('this_is_a_word') == ['this','is','a','word']
assert chunk_name('WHOAREU') == ['WHOAREU']
assert chunk_name('WHO_ARE_U') == ['WHO','ARE','U']
assert chunk_name('XMLIsDerpy') == ['XML','Is','Derpy']
assert chunk_name('fancyURLOpener') == ['fancy','URL','Opener']

def count(d, k):
    assert k
    k = k.lower()
    if k not in d:
        d[k] = 1
    else:
        d[k] += 1
    return

def count2(d, k1, k2):
    k = (k1.lower(), k2.lower())
    if k not in d:
        d[k] = 1
    else:
        d[k] += 1
    return

def show(d, n=1000):
    for (k,v) in sorted(d.iteritems(), key=lambda (k,v):v, reverse=True):
        print ' ', v, k
        n -= 1
        if n == 0: break
    print
    return

def show2(d, n=1000):
    for (k,v) in sorted(d.iteritems(), key=lambda (k,v):v, reverse=True):
        print ' ', v, ' '.join(k)
        n -= 1
        if n == 0: break
    print
    return

def main(argv):
    import fileinput
    var_prefix = {}
    var_suffix = {}
    var_word = {}
    var_ngram = {}
    type_prefix = {}
    type_suffix = {}
    type_word = {}
    type_ngram = {}
    func_prefix = {}
    func_suffix = {}
    func_word = {}
    func_ngram = {}
    func_verb = {}
    for line in fileinput.input():
        (k,_,v) = line.strip().partition(' ')
        if k == 'vardecl':
            words = chunk_name(v)
            if words:
                if 2 <= len(words):
                    count(var_prefix, words[0])
                    count(var_suffix, words[-1])
                for w in words:
                    count(var_word, w)
                for (w1,w2) in zip(words[:-1], words[1:]):
                    count2(var_ngram, w1,w2)
        elif k == 'typedecl':
            words = chunk_name(v)
            if words:
                if 2 <= len(words):
                    count(type_prefix, words[0])
                    count(type_suffix, words[-1])
                for w in words:
                    count(type_word, w)
                for (w1,w2) in zip(words[:-1], words[1:]):
                    count2(type_ngram, w1,w2)
        elif k == 'funcdecl' or k == 'funcall':
            (name,_,args) = v.partition(' ')
            words = chunk_name(name)
            if words:
                if 2 <= len(words):
                    count(func_prefix, words[0])
                    count(func_suffix, words[-1])
                    verbs = (words[0], words[-1])
                else:
                    verbs = (words[-1],)
                for w in words:
                    count(func_word, w)
                for (w1,w2) in zip(words[:-1], words[1:]):
                    count2(func_ngram, w1,w2)
                for noun in args.split(' '):
                    words = chunk_name(noun)
                    if words:
                        n = words[-1]
                        for v in verbs:
                            count2(func_verb, v, n)
    #
    print '+var_prefix:'
    show(var_prefix)
    print '+var_suffix:'
    show(var_suffix)
    print '+var_word:'
    show(var_word)
    print '+var_ngram:'
    show2(var_ngram)
    #
    print '+type_prefix:'
    show(type_prefix)
    print '+type_suffix:'
    show(type_suffix)
    print '+type_word:'
    show(type_word)
    print '+type_ngram:'
    show2(type_ngram)
    #
    print '+func_prefix:'
    show(func_prefix)
    print '+func_suffix:'
    show(func_suffix)
    print '+func_word:'
    show(func_word)
    print '+func_ngram:'
    show2(func_ngram)
    print '+func_verb:'
    show2(func_verb)
    return

if __name__ == '__main__': sys.exit(main(sys.argv))
