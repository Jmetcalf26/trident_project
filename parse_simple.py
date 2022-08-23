import clang.cindex
import ast


def print_ast(node, depth):
    """ Find all references to the type named 'typename'
    """
    print(' '*depth, node.spelling, str(node.kind)[11:])
    #print(' '*depth, node.type.kind)
    #print(' '*depth, node.type.spelling)

    #print(node.location)
    # Recurse for children of this node
    for c in node.get_children():
        print_ast(c, depth+1)


# create the index
index = clang.cindex.Index.create()
# create the translation unit
tu = index.parse("simple.c")
print("Translation Unit:", tu.spelling)
# get the root cursor
root = tu.cursor
print_ast(root, 0)
