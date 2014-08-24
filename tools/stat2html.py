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

def cap(w):
    return w[0].upper()+w[1:]

HEADERS = ('Word','Prefix','Suffix','Bigram')
def listwords(tables,n=10):
    print '<table class=list>'
    print '<tr><th>#</th>'
    for (col,h) in enumerate(HEADERS[:len(tables)]):
        print '<th class=col_%d>%s</th>' % (col,h)
    print '</tr>'
    i = 1
    for row in zip(*tables)[:n]:
        r = [('<td class=order>%d.</td>' % i)]
        for (col,(w,n)) in enumerate(row):
            r.append('<td class="col_%d word"><a href="javascript:void(0);" title="%d occurrences">%s</a></td>' % (col, n, q(w)))
        print '<tr>%s</tr>' % ''.join(r)
        i += 1
    print '</table>'
    return

def listlang(langs,n=10):
    print '<table class=list>'
    print '<tr><th>#</th>'
    names = [ name for (name,_) in langs ]
    tables = [ d for (_,d) in langs ]
    for name in names:
        print '<th class=col_%s>%s</th>' % (name.lower(), name)
    print '</tr>'
    i = 1
    for row in zip(*tables)[:n]:
        r = [('<td class=order>%d.</td>' % i)]
        for (name,(w,n)) in zip(names, row):
            r.append('<td class="col_%s word"><a href="javascript:void(0);" title="%d occurrences">%s</a></td>' % (name.lower(), n, q(w)))
        print '<tr>%s</tr>' % ''.join(r)
        i += 1
    print '</table>'
    return

def listphrases(verb,assoc,n=10):
    print '<table class=list>'
    print '<tr><th>#</th>'
    print '<th class=col_phrase>Verb+Noun</th>'
    print '<th class=col_related>Related Nouns</th>'
    print '</tr>'
    i = 1
    COLS = ('phrase', 'related')
    for row in zip(verb, assoc)[:n]:
        r = [('<td class=order>%d.</td>' % i)]
        for (col,(w,n)) in zip(COLS,row):
            (w1,_,w2) = w.partition(' ')
            if col == 'phrase':
                w = '%s %s.' % (cap(w1),cap(w2))
            else:
                w = '%s, %s' % (cap(w1),cap(w2))
            r.append('<td class="col_%s word"><a href="javascript:void(0);" title="%d occurrences">%s</a></td>' % (col, n, q(w)))
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
            d[key].append((cap(w),int(n)))
    fp.close()
    return d

def fmtpairs(words, fmt):
    r = []
    for (w,n) in words:
        (w1,_,w2) = w.partition(' ')
        r.append((fmt % (w1,w2), n))
    return r

def main(argv):
    langs = []
    for path in argv[1:]:
        d = readlist(path)
        if '-java.' in path:
            name = 'Java'
        elif '-c.' in path:
            name = 'C'
        elif '-py.' in path:
            name = 'Python'
        langs.append((name, d))

    print '''<html><head>
<style><!--
table.list { border: 2px gray solid; border-spacing: 0px; border-collapse: collapse; }
.category { font-size: 100%; font-weight: bold; padding-bottom: 0.5em; }
.nav { font-size: 80%; }
.col_java { background: #ddffff; }
.col_python { background: #ffffdd; }
.col_c { background: #ffddff; }
.col_0 { background: #ffdddd; }
.col_1 { background: #eeeeee; }
.col_2 { background: #eeeeee; }
.col_phrase { background: #ddffdd; }
.col_related { background: #ddddff; }
h1 { color: white; background: #442222; }
h2 { border-bottom: 4px red solid; }
th { border: 2px gray solid; }
td.tab { padding: 1em; }
td.order { border: 2px gray solid; text-align: right; }
td.word { border: 2px gray solid; padding: 0.2em; font-weight: bold; }
--></style>
</head><body>'''
    print '<h1>Result: Quest for True Names</h1>'
    print '<p><a href="https://github.com/euske/github-data-2014">Project Repository</a>'
    print
    print '<h2>Comparison between Languages</h2>'
    print '<h3>Which Word is Commonly Used for Names?</h3>'
    print '<div class=nav>(Hover over a word to see the frequency.)</div>'
    print '<table><tr><td class=tab>'
    print '<div class=category>Variables</div>'
    listlang([ (name, d['var_word']) for (name, d) in langs ])
    print '</td><td class=tab><div class=category>Types/Classes</div>'
    listlang([ (name, d['type_word']) for (name, d) in langs ])
    print '</td><td class=tab><div class=category>Functions/Methods</div>'
    listlang([ (name, d['func_word']) for (name, d) in langs ])
    print '</td></tr></table>'
    print
    for (name, d) in langs:
        print '<h2 class=col_%s>Top Words in %s</h2>' % (name,name)
        print '<table><tr>'
        print '<td class=tab><div class=category>Variable (<em>noun</em>)</div>'
        listwords((d['var_word'], d['var_prefix'], d['var_suffix'], d['var_bigram']))
        print '</td>'
        print '<td class=tab><div class=category>Type/Class</div>'
        listwords((d['type_word'], d['type_prefix'], d['type_suffix'], d['type_bigram']))
        print '</td>'
        print '</tr></table>'
        print '<table><tr>'
        print '<td class=tab><div class=category>Function/Method (<em>verb</em>)</div>'
        listwords((d['func_word'], d['func_prefix'], d['func_suffix'], d['func_bigram']))
        print '</td>'
        print '<td class=tab><div class=category>Combination</div>'
        listphrases(d['func_verb'], d['func_assoc'])
        print '</td>'
        print '</tr></table>'
        print
    print '<hr><address>Yusuke Shinyama</address>'
    print '</body></html>'
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
