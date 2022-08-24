import clang.cindex
from ast import *

def create_ast_node(n):
    node = Constant()
    tokens = list(n.get_tokens())
    node.value = int(tokens[0].spelling)
    print("new created node:", dump(node), end=' ') 
    return node

def rec_ast_node(n, depth):
    if len(list(n.get_children())) == 0:
        print("leaf node")
    else:
        print(' '*depth, str(n.kind)[11:], end=' ')
        child_list = list(n.get_children())

    
def print_ast(node, depth):
    # print out information about the node, including the tokens that it corresponds to
    print(' '*depth, str(node.kind)[11:], end=' ')
    # simple check to see if this is a simple enough node to turn into an ast node
    if str(node.kind)[11:] == 'INTEGER_LITERAL':
        new_node = create_ast_node(node)

    print("num children:", len(list(node.get_children())), end=' ')
    print("tokens:", end=' ')
    for t in node.get_tokens():
        print(t.spelling, end=' ')
    print()

    # Recurse for children of this node
    for c in node.get_children():
        print_ast(c, depth+1)


# create the index
index = clang.cindex.Index.create()
# create the translation unit
tu = index.parse("simple.c")
print("Translation Unit:", tu.spelling, '\n')
# get the root cursor
root = tu.cursor
print_ast(root, 0)

rec_ast_node(root, 0)
print()

print(dump(parse(open('simple.py').read())))

# print(dump(parse('not 3', mode='eval')))
# print(dump(parse('3', mode='eval')))
# print(dump(parse('print(3)', mode='eval')))
# a = parse('123', mode='eval')
# print(a)
# a = parse('not 3', mode='eval')
# print(a)

# node = UnaryOp()
# node.op = USub()
# node.operand = Constant()
# node.operand.value = 5
# node.operand.lineno = 0
# node.operand.col_offset = 0
# node.lineno = 0
# node.col_offset = 0

# print(node)
# print(dump(node))


