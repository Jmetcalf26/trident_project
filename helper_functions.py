from ast import *

def add_main_check(rn):
    i = If()
    i.test = Compare()
    i.test.left = Name()
    i.test.left.id = '__name__'
    i.test.left.ctx = Load()
    i.test.ops = []
    i.test.ops = [Eq()]
    c = Constant()
    c.value = '__main__'
    c.kind = None
    i.test.comparators = [c]
    e = Expr()
    ca = Call()
    n = Name()
    n.id = 'main'
    n.ctx = Load()
    ca.func = n
    ca.args = []
    ca.keywords = []
    e.value = ca
    i.body = [e]
    i.orelse = []
    rn.body.append(i)
    return rn

def add_args():
    e = []
    n = None
    return arguments(e, e, n, e, e, n, e)

    # posonlyargs = []
    # args = []
    # vararg = None
    # kwonlyargs = []
    # kw_defaults = []
    # kwarg = None
    # defaults = []
    # return arguments(posonlyargs, args, vararg, kwonlyargs, kw_defaults, kwarg, defaults)

def stars():
    print("\n"+"*"*50)


def print_c_ast(n, depth): 
    nt = str(n.kind)[11:]
    print((' '*depth) + nt, end=' ')
    print("|".join(t.spelling for t in n.get_tokens()))
    # for t in n.get_tokens():
    #     print(t.spelling, end=' ')
    # print()

    for c in n.get_children():
        print_c_ast(c, depth+1)
