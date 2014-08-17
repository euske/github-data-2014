#!/usr/bin/env python
import sys
import zipfile
import compiler
from compiler import ast

def register_var(name):
    print 'vardecl', name
    return
def register_func(name, args):
    print 'funcdecl', name, ' '.join(args)
    return
def register_class(name):
    print 'typedecl', name
    return
def funcall(name, args):
    print 'funcall', name, ' '.join( arg or '*' for arg in args )
    return

def getname(tree):
    if isinstance(tree, ast.Name):
        return tree.name
    elif isinstance(tree, ast.Getattr):
        return tree.attrname
    elif isinstance(tree, ast.Subscript):
        return getname(tree.expr)
    elif isinstance(tree, ast.Slice):      
        return getname(tree.expr)
    elif isinstance(tree, (ast.UnaryAdd, ast.UnarySub, ast.Invert)):
        return getname(tree.expr)
    return None

def traverse(tree):

    if tree is None:
        pass

    elif isinstance(tree, ast.Module):
        traverse(tree.node)
      
    # global
    elif isinstance(tree, ast.Global):
        for name in tree.names:
            register_var(name)

    # def
    elif isinstance(tree, ast.Function):
        register_func(tree.name, tree.argnames)
        traverse(tree.code)
        
    # class
    elif isinstance(tree, ast.Class):
        register_class(tree.name)
        traverse(tree.code)
    # assign
    elif isinstance(tree, ast.Assign):
        for node in tree.nodes:
            traverse(tree.expr)
            traverse(node)
    elif isinstance(tree, ast.AugAssign):
        traverse(tree.expr)
    elif isinstance(tree, ast.AssTuple):
        for c in tree.nodes:
            traverse(c)
    elif isinstance(tree, ast.AssList):
        for c in tree.nodes:
            traverse(c)
    elif isinstance(tree, ast.AssName):
        register_var(tree.name)
    elif isinstance(tree, ast.AssAttr):
        pass
    elif isinstance(tree, ast.Subscript):
        traverse(tree.expr)
        for sub in tree.subs:
            traverse(sub)

    # return
    elif isinstance(tree, ast.Return):
        traverse(tree.value)

    # yield (for both python 2.4 and 2.5)
    elif isinstance(tree, ast.Yield):
        traverse(tree.value)

    # with (for __future__ python 2.5 or 2.6)
    elif isinstance(tree, ast.With):
        traverse(tree.expr)
        traverse(tree.vars)
        traverse(tree.body)

    # (mutliple statements)
    elif isinstance(tree, ast.Stmt):
        for stmt in tree.nodes:
            traverse(stmt)

    # if, elif, else
    elif isinstance(tree, ast.If):
        for (expr,stmt) in tree.tests:
            traverse(expr)
            traverse(stmt)
        if tree.else_:
            traverse(tree.else_)

    # for
    elif isinstance(tree, ast.For):
        traverse(tree.list)
        traverse(tree.assign)
        traverse(tree.body)
        if tree.else_:
            traverse(tree.else_)

    # while
    elif isinstance(tree, ast.While):
        traverse(tree.test)
        traverse(tree.body)
        if tree.else_:
            traverse(tree.else_)

    # try ... except
    elif isinstance(tree, ast.TryExcept):
        traverse(tree.body)
        for (expr,e,stmt) in tree.handlers:
            if expr:
                traverse(expr)
            if e:
                traverse(e)
            traverse(stmt)
        if tree.else_:
            traverse(tree.else_)

    # try ... finally
    elif isinstance(tree, ast.TryFinally):
        traverse(tree.body)
        traverse(tree.final)

    # raise
    elif isinstance(tree, ast.Raise):
        if tree.expr1:
            traverse(tree.expr1)
        if tree.expr2:
            traverse(tree.expr2)
        
    # import
    elif isinstance(tree, ast.Import):
        pass
    # from
    elif isinstance(tree, ast.From):
        pass

    # print, printnl
    elif isinstance(tree, (ast.Print, ast.Printnl)):
        for node in tree.nodes:
            traverse(node)
    
    # discard
    elif isinstance(tree, ast.Discard):
        traverse(tree.expr)

    # other statements
    elif isinstance(tree, ast.Break):
        pass
    elif isinstance(tree, ast.Continue):
        pass
    elif isinstance(tree, ast.Print):
        pass
    elif isinstance(tree, ast.Yield):
        pass
    elif isinstance(tree, ast.Pass):
        pass
    elif isinstance(tree, ast.Exec):
        pass

    # expressions
    elif isinstance(tree, ast.Const):
        pass
    elif isinstance(tree, ast.Name):
        pass
    elif isinstance(tree, ast.CallFunc):
        funcall(getname(tree.node), [ getname(n) for n in tree.args ])
        traverse(tree.node)
        for arg1 in tree.args:
            traverse(arg1)
        if tree.star_args:
            traverse(tree.star_args)
        if tree.dstar_args:
            traverse(tree.dstar_args)
    elif isinstance(tree, ast.Keyword):
        traverse(tree.expr)
    elif isinstance(tree, ast.Getattr):
        traverse(tree.expr)
    elif isinstance(tree, ast.Slice):      
        traverse(tree.expr)
        if tree.lower:
            traverse(tree.lower)
        if tree.upper:
            traverse(tree.upper)
    elif isinstance(tree, ast.Sliceobj):
        for node in tree.nodes:
            traverse(node)
    elif isinstance(tree, ast.Tuple):
        for node in tree.nodes:
            traverse(node)
    elif isinstance(tree, ast.List):
        for node in tree.nodes:
            traverse(node)
    elif isinstance(tree, ast.Set):
        for node in tree.nodes:
            traverse(node)
    elif isinstance(tree, ast.Dict):
        for (k,v) in tree.items:
            traverse(k)
            traverse(v)
    elif isinstance(tree, (ast.Add, ast.Sub, ast.Mul, ast.Div,
                           ast.Mod, ast.FloorDiv, ast.Power,
                           ast.LeftShift, ast.RightShift)):
        traverse(tree.left)
        traverse(tree.right)
    elif isinstance(tree, ast.Compare):
        traverse(tree.expr)
        for (_,node) in tree.ops:
            traverse(node)
    elif isinstance(tree, (ast.UnaryAdd, ast.UnarySub, ast.Invert)):
        traverse(tree.expr)
    elif isinstance(tree, (ast.And, ast.Or,
                           ast.Bitand, ast.Bitor, ast.Bitxor)):
        for node in tree.nodes:
            traverse(node)
    elif isinstance(tree, ast.Not):
        traverse(tree.expr)
    elif isinstance(tree, ast.Lambda):
        for value in tree.defaults:
            traverse(value)
        traverse(tree.code)
    elif isinstance(tree, ast.IfExp):
        traverse(tree.test)
        traverse(tree.then)
        traverse(tree.else_)
    elif isinstance(tree, ast.Backquote):
        traverse(tree.expr)

    # list comprehension
    elif isinstance(tree, ast.ListComp):
        traverse(tree.expr)
        for qual in tree.quals:
            traverse(qual.list)
            traverse(qual.assign)
            for qif in qual.ifs:
                traverse(qif.test)
    
    # generator expression
    elif isinstance(tree, ast.GenExpr):
        gen = tree.code
        traverse(gen.expr)
        for qual in gen.quals:
            traverse(qual.iter)
            traverse(qual.assign)
            for qif in qual.ifs:
                traverse(qif.test)

    # Assert
    elif isinstance(tree, ast.Assert):
        traverse(tree.test)
        if tree.fail:
            traverse(tree.fail)
    
    # Ellipsis
    elif isinstance(tree, ast.Ellipsis):
        pass
    
    else:
        raise SyntaxError('unsupported syntax: %r (%r)' % (tree, tree.lineno))
    return

def main(argv):
    args = argv[1:]
    for path in args:
        if path.endswith('.zip'):
            zf = zipfile.ZipFile(path)
            for name in zf.namelist():
                sys.stderr.write('parsing: %r\n' % name)
                sys.stderr.flush()
                data = zf.read(name)
                try:
                    tree = compiler.parse(data)
                    traverse(tree)
                except SyntaxError, e:
                    print 'error:', name, e
            zf.close()
        else:
            sys.stderr.write('parsing: %r\n' % path)
            sys.stderr.flush()
            fp = open(path, 'rb')
            data = fp.read()
            try:
                tree = compiler.parse(data)
                traverse(tree)
            except SyntaxError, e:
                print 'error:', name, e
            fp.close()
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
