#!/usr/bin/env python
import sys

# quote HTML metacharacters.
def q(s):
    assert isinstance(s, basestring), s
    return (s.
            replace('&','&amp;').
            replace('>','&gt;').
            replace('<','&lt;').
            replace('"','&#34;').
            replace("'",'&#39;'))

HEADERS = ('Word','Prefix','Suffix','Bigram')
def listwords(tables,n=10):
    print '<table class=list>'
    print '<tr><th>#</th>'
    for (col,h) in enumerate(HEADERS[:len(tables)]):
        print '<th class=col_%d colspan=2>%s</th>' % (col,h)
    print '</tr>'
    i = 1
    for row in zip(*tables)[:n]:
        r = [('<td class=order>%d.</td>' % i)]
        for (col,(w,n)) in enumerate(row):
            r.append('<td class="col_%d word"><code>%s</code></td>' % (col, q(w)))
            r.append('<td class="col_%d count">%d</td>' % (col, n))
        print '<tr>%s</tr>' % ''.join(r)
        i += 1
    print '</table>'
    return

def listphrases(verb,assoc,n=10):
    print '<table class=list>'
    print '<tr><th>#</th>'
    print '<th class=col_phrase colspan=2>Verb+Noun</th>'
    print '<th class=col_related colspan=2>Related Nouns</th>'
    print '</tr>'
    i = 1
    COLS = ('phrase', 'related')
    for row in zip(verb, assoc)[:n]:
        r = [('<td class=order>%d.</td>' % i)]
        for (col,(w,n)) in zip(COLS,row):
            (w1,_,w2) = w.partition(' ')
            if col == 'phrase':
                w = '%s %s.' % (w1[0].upper()+w1[1:], w2)
            else:
                w = '%s, %s' % (w1,w2)
            r.append('<td class="col_%s word"><code>%s</code></td>' % (col,q(w)))
            r.append('<td class="col_%s count">%d</td>' % (col, n))
        print '<tr>%s</tr>' % ''.join(r)
        i += 1
    print '</table>'
    return

def readlist(path):
    fp = file(path)
    d = {}
    for line in fp:
        line = line.strip()
        if line.startswith('+'):
            key = line[1:-1]
            d[key] = []
        elif line:
            (n,_,w) = line.partition(' ')
            d[key].append((w,int(n)))
    fp.close()
    return d

def fmtpairs(words, fmt):
    r = []
    for (w,n) in words:
        (w1,_,w2) = w.partition(' ')
        r.append((fmt % (w1,w2), n))
    return r

def main(argv):
    print '''<html><head>
<style><!--
table.list { border: 1px gray solid; }
div.category { font-size: 100%; font-weight: bold; padding-bottom: 0.5em; }
.col_0 { background: #ffddff; }
.col_1 { background: #eeeeee; }
.col_2 { background: #eeeeee; }
.col_phrase { background: #ddffdd; }
.col_related { background: #ddddff; }
th { border-bottom: 2px gray solid; border-right: 2px gray solid; }
td { padding: 0.2em; }
td.order { border-right: 2px gray solid; text-align: right; }
td.count { border-right: 2px gray solid; text-align: right; padding-right: 0.5em; }
td.word { font-weight: bold; }
--></style>
</head><body>'''
    for path in argv[1:]:
        d = readlist(path)
        print '<h1>Top Names for %s</h1>' % path
        print '<table><tr>'
        print '<td><div class=category>Variable (noun)</div>'
        listwords((d['var_word'], d['var_prefix'], d['var_suffix'], d['var_bigram']))
        print '</td>'
        print '<td><div class=category>Type/Class</div>'
        listwords((d['type_word'], d['type_prefix'], d['type_suffix'], d['type_bigram']))
        print '</td>'
        print '</tr></table>'
        print '<table><tr>'
        print '<td><div class=category>Function/Method (verb)</div>'
        listwords((d['func_word'], d['func_prefix'], d['func_suffix'], d['func_bigram']))
        print '</td>'
        print '<td><div class=category>Combination</div>'
        listphrases(d['func_verb'], d['func_assoc'])
        print '</td>'
        print '</tr></table>'
        print
    print '</body></html>'
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
