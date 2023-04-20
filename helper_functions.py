from ast import *
from enum import Enum
from clang.cindex import TypeKind, CursorKind, BinaryOperator


def is_LValueToRValue(node):
    l_values = [CursorKind.DECL_REF_EXPR, CursorKind.ARRAY_SUBSCRIPT_EXPR, CursorKind.UNARY_OPERATOR]
    return list(node.get_children())[0].kind in l_values
def is_FunctionToPointerDecay(node):
    return node.referenced is not None and node.referenced.kind == CursorKind.FUNCTION_DECL
def is_ArrayToPointerDecay(node):
    array_values = [TypeKind.CONSTANTARRAY, TypeKind.VARIABLEARRAY, TypeKind.DEPENDENTSIZEDARRAY, TypeKind.INCOMPLETEARRAY]
    return node.type.get_canonical().kind == TypeKind.POINTER and list(node.get_children())[0].type.get_canonical().kind in array_values
def is_NoOp(node):
    return node.type.get_canonical().spelling == "const char *" and list(node.get_children())[0].type.get_canonical().spelling == "char *"
 

def bin(a):
    print("{0:b}".format(a))

def is_child(children, node_type):
    for c in children:
        if str(c.kind)[11:] == node_type:
            return True
    return False
            
def sizeof(cute_little_decoration, size):
    return size

def add_overflow_check(n, node):
    stars()
    print("INSIDE INT ERROR CHECK")
    stars()
    #largest_value_of_data_size = 2 ** max_place_value - 1
    #smallest_value_of_data_size = 2 ** min_place_value - 1
    #if value > largest_value_of_data_size:
    node = Module([node], [])
    if get_type(n) == "INT":
       check = If(Compare(Name(n.spelling), [Gt()], [Constant((2 ** 31) -1)]), [Expr([Call(Name('print'), [Constant('NOOOO')], [])])], [])
       check.orelse.append(If(Compare(Name(n.spelling), [Lt()], [Constant( -2 ** 31 )]), [Expr([Call(Name('print'), [Constant('NOOOO')], [])])], []))
       node.body.append(check)

    if get_type(n) == "UINT":
       check = If(Compare(Name(n.spelling), [Gt()], [Constant((2 ** 32) -1)]), [Expr([Call(Name('print'), [Constant('NOOOO')], [])])], [])
       node.body.append(check)

    stars()
    print("LEAVING INT ERROR CHECK")
    stars()
    return node

def print_node_info(n):
    print("n.displayname", n.displayname)
    print("n.kind", n.kind)
    print("n.spelling", n.spelling)
    #if "ARRAY" in str(n.type.get_canonical().kind):
    #print('element_type:', n.type.element_type.spelling)
    #print('element_type size:', n.type.element_type.get_size())
    #print('element_count:', n.type.element_count)
    #print('get_array_element_type:', n.type.get_array_element_type().spelling)
    #print('get_array_element_type size:', n.type.get_array_element_type().get_size())
    print('get_canonical().spelling:', n.type.get_canonical().spelling)
    print('get_canonical().kind:', n.type.get_canonical().kind)
    #print('get_class_type():', n.type.get_class_type().kind.spelling)
    print('get_size():', n.type.get_size())
    #print('get_pointee().kind:', n.type.get_pointee().kind)
    #print('get_pointee().kind.spelling:', n.type.get_pointee().kind.spelling)
    #print('get_pointee().spelling:', n.type.get_pointee().spelling)
    #print('get_pointee().get_size():', n.type.get_pointee().get_size())
    #print('get_pointee().get_array_element_type().size:', n.type.get_pointee().get_array_element_type().get_size())
    num_args = len(list(n.get_arguments()))
    print('num_args:', num_args)
    children = list(n.get_children())
    print('num_children:', len(children))
    tokens = list(n.get_tokens())
    print('num_tokens:', len(tokens))
    print("arguments:", end=' ')
    for a in n.get_arguments():
        print(a.spelling, end=' ')
    print()

    print('children:')
    for c in children:
        print('  '+str(c.kind)[11:], c.spelling)
    #print("|".join(t.spelling for t in n.get_tokens()))
    return

def get_type(node):
    return str(node.type.get_canonical().kind)[9:]

TypeCat = Enum('TypeCat', 'INTEGRAL FLOATING POINTER UNKNOWN')

def type_category(node):
    return {
        TypeKind.BLOCKPOINTER: TypeCat.POINTER,
        TypeKind.CONSTANTARRAY: TypeCat.POINTER,
        TypeKind.DEPENDENTSIZEDARRAY: TypeCat.POINTER,
        TypeKind.INCOMPLETEARRAY: TypeCat.POINTER,
        TypeKind.MEMBERPOINTER: TypeCat.POINTER,
        TypeKind.NULLPTR: TypeCat.POINTER,
        TypeKind.POINTER: TypeCat.POINTER,
        TypeKind.VARIABLEARRAY: TypeCat.POINTER,

        TypeKind.BOOL: TypeCat.INTEGRAL,
        TypeKind.CHAR16: TypeCat.INTEGRAL,
        TypeKind.CHAR32: TypeCat.INTEGRAL,
        TypeKind.ENUM: TypeCat.INTEGRAL,
        TypeKind.INT: TypeCat.INTEGRAL,
        TypeKind.INT128: TypeCat.INTEGRAL,
        TypeKind.LONG: TypeCat.INTEGRAL,
        TypeKind.LONGLONG: TypeCat.INTEGRAL,
        TypeKind.SCHAR: TypeCat.INTEGRAL,
        TypeKind.SHORT: TypeCat.INTEGRAL,
        TypeKind.UCHAR: TypeCat.INTEGRAL,
        TypeKind.UINT: TypeCat.INTEGRAL,
        TypeKind.UINT128: TypeCat.INTEGRAL,
        TypeKind.ULONG: TypeCat.INTEGRAL,
        TypeKind.ULONGLONG: TypeCat.INTEGRAL,
        TypeKind.USHORT: TypeCat.INTEGRAL,
        TypeKind.WCHAR: TypeCat.INTEGRAL,

        TypeKind.COMPLEX: TypeCat.FLOATING,
        TypeKind.DOUBLE: TypeCat.FLOATING,
        TypeKind.FLOAT: TypeCat.FLOATING,
        TypeKind.FLOAT128: TypeCat.FLOATING,
        TypeKind.LONGDOUBLE: TypeCat.FLOATING,
    }.get(node.kind, TypeCat.UNKNOWN)

def translate_u_operator(operator):
    op = None 
    if operator == '!':
        op = Not()
    elif operator == '-':
        op = USub()
    elif operator == '+':
        op = UAdd()
    elif operator == '~':
        op = Invert()
    return op

def translate_operator(operator, lhs_cat=TypeCat.UNKNOWN, rhs_cat=TypeCat.UNKNOWN):
    op = None 
    # Relational Operators
    if operator == BinaryOperator.EQ:
        op = Eq()
    if operator == BinaryOperator.NE:
        op = NotEq()
    if operator == BinaryOperator.LT:
        op = Lt()
    if operator == BinaryOperator.LE:
        op = LtE()
    if operator == BinaryOperator.GT:
        op = Gt()
    if operator == BinaryOperator.GE:
        op = GtE()
    # Arithmetic Operators
    if operator == BinaryOperator.Add:
        op = Add()
    elif operator == BinaryOperator.Sub:
        op = Sub()
    elif operator == BinaryOperator.Mul:
        op = Mult()
    elif operator == BinaryOperator.Div:
        if lhs_cat is TypeCat.FLOATING or rhs_cat is TypeCat.FLOATING:
            op = FloorDiv()
        else:
            op = Div()
    # THIS WILL NEVER BE REACHED BECAUSE THERE IS NONE OF THIS IN C, ADD CHECK TO SEE IF BOTH SIDES ARE INTS TO USE THIS!
    # (done - see above)
    #elif operator == '//':
        #op = FloorDiv()
    elif operator == BinaryOperator.Rem:
        op = Mod()
    # SAME WITH THIS ONE
    #elif operator == '**':
        #op = Pow()
    elif operator == BinaryOperator.Shl:
        op = LShift()
    elif operator == BinaryOperator.Shr:
        op = RShift()
    elif operator == BinaryOperator.Or:
        op = BitOr()
    elif operator == BinaryOperator.Xor:
        op = BitXor()
    elif operator == BinaryOperator.And:
        op = BitAnd()
    elif operator == BinaryOperator.LAnd:
        op = And()
    elif operator == BinaryOperator.LOr:
        op = Or()

    # maybe add this one? I don't know, but it's present in the python ast library
    # elif operator == '@':
    #     op = MatMult()
    return op

def add_main_check():
    return If(Compare(Name('__name__', Load()), [Eq()], [Constant('__main__')]), [Expr(Call(Name('main', Load()), [], []))], [])

# def add_pointer_class():
#     #  class ast.ClassDef(name, bases, keywords, starargs, kwargs, body, decorator_list)
#     cd = ClassDef('Pointer', [], [], decorator_list=[])
#     fd = FunctionDef('_init__', arguments([], [arg('self'), arg('array'), arg('index')], defaults=[]), [Assign([Attribute(Name('self', Load()), 'array', Store())], Name('array', Load())), Assign([Attribute(Name('self', Load()), 'index', Store())], Name('index', Load()))], [])
#     fd2 = FunctionDef('get', arguments([], [], defaults=[]), [Return(Subscript(Attribute(Name('self', Load()), 'array', Load()), Attribute(Name('self', Load()), 'index', Load()), Load()))], [])
#     cd.body = [fd, fd2]
#     return cd

def add_helper_classes():
    cd = ImportFrom(
            module='helper_classes',
            names=[alias(name='*')],
            level=0)
    return cd

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

preprocessing = ['__llvm__', '__clang__', '__clang_major__', '__clang_minor__', '__clang_patchlevel__', '__clang_version__', '__GNUC__', '__GNUC_MINOR__', '__GNUC_PATCHLEVEL__', '__GXX_ABI_VERSION', '__ATOMIC_RELAXED', '__ATOMIC_CONSUME', '__ATOMIC_ACQUIRE', '__ATOMIC_RELEASE', '__ATOMIC_ACQ_REL', '__ATOMIC_SEQ_CST', '__OPENCL_MEMORY_SCOPE_WORK_ITEM', '__OPENCL_MEMORY_SCOPE_WORK_GROUP', '__OPENCL_MEMORY_SCOPE_DEVICE', '__OPENCL_MEMORY_SCOPE_ALL_SVM_DEVICES', '__OPENCL_MEMORY_SCOPE_SUB_GROUP', '__PRAGMA_REDEFINE_EXTNAME', '__VERSION__', '__OBJC_BOOL_IS_BOOL', '__CONSTANT_CFSTRINGS__', '__ORDER_LITTLE_ENDIAN__', '__ORDER_BIG_ENDIAN__', '__ORDER_PDP_ENDIAN__', '__BYTE_ORDER__', '__LITTLE_ENDIAN__', '_LP64', '__LP64__', '__CHAR_BIT__', '__SCHAR_MAX__', '__SHRT_MAX__', '__INT_MAX__', '__LONG_MAX__', '__LONG_LONG_MAX__', '__WCHAR_MAX__', '__WINT_MAX__', '__INTMAX_MAX__', '__SIZE_MAX__', '__UINTMAX_MAX__', '__PTRDIFF_MAX__', '__INTPTR_MAX__', '__UINTPTR_MAX__', '__SIZEOF_DOUBLE__', '__SIZEOF_FLOAT__', '__SIZEOF_INT__', '__SIZEOF_LONG__', '__SIZEOF_LONG_DOUBLE__', '__SIZEOF_LONG_LONG__', '__SIZEOF_POINTER__', '__SIZEOF_SHORT__', '__SIZEOF_PTRDIFF_T__', '__SIZEOF_SIZE_T__', '__SIZEOF_WCHAR_T__', '__SIZEOF_WINT_T__', '__SIZEOF_INT128__', '__INTMAX_TYPE__', '__INTMAX_FMTd__', '__INTMAX_FMTi__', '__INTMAX_C_SUFFIX__', '__UINTMAX_TYPE__', '__UINTMAX_FMTo__', '__UINTMAX_FMTu__', '__UINTMAX_FMTx__', '__UINTMAX_FMTX__', '__UINTMAX_C_SUFFIX__', '__INTMAX_WIDTH__', '__PTRDIFF_TYPE__', '__PTRDIFF_FMTd__', '__PTRDIFF_FMTi__', '__PTRDIFF_WIDTH__', '__INTPTR_TYPE__', '__INTPTR_FMTd__', '__INTPTR_FMTi__', '__INTPTR_WIDTH__', '__SIZE_TYPE__', '__SIZE_FMTo__', '__SIZE_FMTu__', '__SIZE_FMTx__', '__SIZE_FMTX__', '__SIZE_WIDTH__', '__WCHAR_TYPE__', '__WCHAR_WIDTH__', '__WINT_TYPE__', '__WINT_WIDTH__', '__SIG_ATOMIC_WIDTH__', '__SIG_ATOMIC_MAX__', '__CHAR16_TYPE__', '__CHAR32_TYPE__', '__UINTMAX_WIDTH__', '__UINTPTR_TYPE__', '__UINTPTR_FMTo__', '__UINTPTR_FMTu__', '__UINTPTR_FMTx__', '__UINTPTR_FMTX__', '__UINTPTR_WIDTH__', '__FLT_DENORM_MIN__', '__FLT_HAS_DENORM__', '__FLT_DIG__', '__FLT_DECIMAL_DIG__', '__FLT_EPSILON__', '__FLT_HAS_INFINITY__', '__FLT_HAS_QUIET_NAN__', '__FLT_MANT_DIG__', '__FLT_MAX_10_EXP__', '__FLT_MAX_EXP__', '__FLT_MAX__', '__FLT_MIN_10_EXP__', '__FLT_MIN_EXP__', '__FLT_MIN__', '__DBL_DENORM_MIN__', '__DBL_HAS_DENORM__', '__DBL_DIG__', '__DBL_DECIMAL_DIG__', '__DBL_EPSILON__', '__DBL_HAS_INFINITY__', '__DBL_HAS_QUIET_NAN__', '__DBL_MANT_DIG__', '__DBL_MAX_10_EXP__', '__DBL_MAX_EXP__', '__DBL_MAX__', '__DBL_MIN_10_EXP__', '__DBL_MIN_EXP__', '__DBL_MIN__', '__LDBL_DENORM_MIN__', '__LDBL_HAS_DENORM__', '__LDBL_DIG__', '__LDBL_DECIMAL_DIG__', '__LDBL_EPSILON__', '__LDBL_HAS_INFINITY__', '__LDBL_HAS_QUIET_NAN__', '__LDBL_MANT_DIG__', '__LDBL_MAX_10_EXP__', '__LDBL_MAX_EXP__', '__LDBL_MAX__', '__LDBL_MIN_10_EXP__', '__LDBL_MIN_EXP__', '__LDBL_MIN__', '__POINTER_WIDTH__', '__BIGGEST_ALIGNMENT__', '__WINT_UNSIGNED__', '__INT8_TYPE__', '__INT8_FMTd__', '__INT8_FMTi__', '__INT8_C_SUFFIX__', '__INT16_TYPE__', '__INT16_FMTd__', '__INT16_FMTi__', '__INT16_C_SUFFIX__', '__INT32_TYPE__', '__INT32_FMTd__', '__INT32_FMTi__', '__INT32_C_SUFFIX__', '__INT64_TYPE__', '__INT64_FMTd__', '__INT64_FMTi__', '__INT64_C_SUFFIX__', '__UINT8_TYPE__', '__UINT8_FMTo__', '__UINT8_FMTu__', '__UINT8_FMTx__', '__UINT8_FMTX__', '__UINT8_C_SUFFIX__', '__UINT8_MAX__', '__INT8_MAX__', '__UINT16_TYPE__', '__UINT16_FMTo__', '__UINT16_FMTu__', '__UINT16_FMTx__', '__UINT16_FMTX__', '__UINT16_C_SUFFIX__', '__UINT16_MAX__', '__INT16_MAX__', '__UINT32_TYPE__', '__UINT32_FMTo__', '__UINT32_FMTu__', '__UINT32_FMTx__', '__UINT32_FMTX__', '__UINT32_C_SUFFIX__', '__UINT32_MAX__', '__INT32_MAX__', '__UINT64_TYPE__', '__UINT64_FMTo__', '__UINT64_FMTu__', '__UINT64_FMTx__', '__UINT64_FMTX__', '__UINT64_C_SUFFIX__', '__UINT64_MAX__', '__INT64_MAX__', '__INT_LEAST8_TYPE__', '__INT_LEAST8_MAX__', '__INT_LEAST8_FMTd__', '__INT_LEAST8_FMTi__', '__UINT_LEAST8_TYPE__', '__UINT_LEAST8_MAX__', '__UINT_LEAST8_FMTo__', '__UINT_LEAST8_FMTu__', '__UINT_LEAST8_FMTx__', '__UINT_LEAST8_FMTX__', '__INT_LEAST16_TYPE__', '__INT_LEAST16_MAX__', '__INT_LEAST16_FMTd__', '__INT_LEAST16_FMTi__', '__UINT_LEAST16_TYPE__', '__UINT_LEAST16_MAX__', '__UINT_LEAST16_FMTo__', '__UINT_LEAST16_FMTu__', '__UINT_LEAST16_FMTx__', '__UINT_LEAST16_FMTX__', '__INT_LEAST32_TYPE__', '__INT_LEAST32_MAX__', '__INT_LEAST32_FMTd__', '__INT_LEAST32_FMTi__', '__UINT_LEAST32_TYPE__', '__UINT_LEAST32_MAX__', '__UINT_LEAST32_FMTo__', '__UINT_LEAST32_FMTu__', '__UINT_LEAST32_FMTx__', '__UINT_LEAST32_FMTX__', '__INT_LEAST64_TYPE__', '__INT_LEAST64_MAX__', '__INT_LEAST64_FMTd__', '__INT_LEAST64_FMTi__', '__UINT_LEAST64_TYPE__', '__UINT_LEAST64_MAX__', '__UINT_LEAST64_FMTo__', '__UINT_LEAST64_FMTu__', '__UINT_LEAST64_FMTx__', '__UINT_LEAST64_FMTX__', '__INT_FAST8_TYPE__', '__INT_FAST8_MAX__', '__INT_FAST8_FMTd__', '__INT_FAST8_FMTi__', '__UINT_FAST8_TYPE__', '__UINT_FAST8_MAX__', '__UINT_FAST8_FMTo__', '__UINT_FAST8_FMTu__', '__UINT_FAST8_FMTx__', '__UINT_FAST8_FMTX__', '__INT_FAST16_TYPE__', '__INT_FAST16_MAX__', '__INT_FAST16_FMTd__', '__INT_FAST16_FMTi__', '__UINT_FAST16_TYPE__', '__UINT_FAST16_MAX__', '__UINT_FAST16_FMTo__', '__UINT_FAST16_FMTu__', '__UINT_FAST16_FMTx__', '__UINT_FAST16_FMTX__', '__INT_FAST32_TYPE__', '__INT_FAST32_MAX__', '__INT_FAST32_FMTd__', '__INT_FAST32_FMTi__', '__UINT_FAST32_TYPE__', '__UINT_FAST32_MAX__', '__UINT_FAST32_FMTo__', '__UINT_FAST32_FMTu__', '__UINT_FAST32_FMTx__', '__UINT_FAST32_FMTX__', '__INT_FAST64_TYPE__', '__INT_FAST64_MAX__', '__INT_FAST64_FMTd__', '__INT_FAST64_FMTi__', '__UINT_FAST64_TYPE__', '__UINT_FAST64_MAX__', '__UINT_FAST64_FMTo__', '__UINT_FAST64_FMTu__', '__UINT_FAST64_FMTx__', '__UINT_FAST64_FMTX__', '__USER_LABEL_PREFIX__', '__FINITE_MATH_ONLY__', '__GNUC_STDC_INLINE__', '__GCC_ATOMIC_TEST_AND_SET_TRUEVAL', '__CLANG_ATOMIC_BOOL_LOCK_FREE', '__CLANG_ATOMIC_CHAR_LOCK_FREE', '__CLANG_ATOMIC_CHAR16_T_LOCK_FREE', '__CLANG_ATOMIC_CHAR32_T_LOCK_FREE', '__CLANG_ATOMIC_WCHAR_T_LOCK_FREE', '__CLANG_ATOMIC_SHORT_LOCK_FREE', '__CLANG_ATOMIC_INT_LOCK_FREE', '__CLANG_ATOMIC_LONG_LOCK_FREE', '__CLANG_ATOMIC_LLONG_LOCK_FREE', '__CLANG_ATOMIC_POINTER_LOCK_FREE', '__GCC_ATOMIC_BOOL_LOCK_FREE', '__GCC_ATOMIC_CHAR_LOCK_FREE', '__GCC_ATOMIC_CHAR16_T_LOCK_FREE', '__GCC_ATOMIC_CHAR32_T_LOCK_FREE', '__GCC_ATOMIC_WCHAR_T_LOCK_FREE', '__GCC_ATOMIC_SHORT_LOCK_FREE', '__GCC_ATOMIC_INT_LOCK_FREE', '__GCC_ATOMIC_LONG_LOCK_FREE', '__GCC_ATOMIC_LLONG_LOCK_FREE', '__GCC_ATOMIC_POINTER_LOCK_FREE', '__NO_INLINE__', '__FLT_EVAL_METHOD__', '__FLT_RADIX__', '__DECIMAL_DIG__', '__GCC_ASM_FLAG_OUTPUTS__', '__code_model_small_', '__amd64__', '__amd64', '__x86_64', '__x86_64__', '__SEG_GS', '__SEG_FS', '__seg_gs', '__seg_fs', '__k8', '__k8__', '__tune_k8__', '__REGISTER_PREFIX__', '__NO_MATH_INLINES', '__FXSR__', '__SSE2__', '__SSE2_MATH__', '__SSE__', '__SSE_MATH__', '__MMX__', '__GCC_HAVE_SYNC_COMPARE_AND_SWAP_1', '__GCC_HAVE_SYNC_COMPARE_AND_SWAP_2', '__GCC_HAVE_SYNC_COMPARE_AND_SWAP_4', '__GCC_HAVE_SYNC_COMPARE_AND_SWAP_8', '__SIZEOF_FLOAT128__', 'unix', '__unix', '__unix__', 'linux', '__linux', '__linux__', '__ELF__', '__gnu_linux__', '__FLOAT128__', '__STDC__', '__STDC_HOSTED__', '__STDC_VERSION__', '__STDC_UTF_16__', '__STDC_UTF_32__']

def print_c_ast(n, depth): 
    nt = str(n.kind)[11:]
    if n.spelling in preprocessing:
        return
    print((' '*depth) + nt, end=' ')
    #print((' '*depth) + nt)
    #print("|".join(t.spelling for t in n.get_tokens()))
    print(n.spelling)
    # for t in n.get_tokens():
    #     print(t.spelling, end=' ')
    # print()

    for c in n.get_children():
        print_c_ast(c, depth+1)

def cursor_bools(n):
    print('n.kind.is_attribute', n.kind.is_attribute())
    print('n.kind.is_declaration', n.kind.is_declaration())
    print('n.kind.is_expression', n.kind.is_expression())
    print('n.kind.is_invalid', n.kind.is_invalid())
    print('n.kind.is_preprocessing', n.kind.is_preprocessing())
    print('n.kind.is_reference', n.kind.is_reference())
    print('n.kind.is_statement', n.kind.is_statement())
    print('n.kind.is_translation_unit', n.kind.is_translation_unit())
    print('n.kind.is_unexposed', n.kind.is_unexposed())

def extended_node_info(n):
    print('n.is_const_method()', n.is_const_method())
    print('n.is_mutable_field()', n.is_mutable_field())
    print('spelling:', n.spelling)
    print('raw_comment:', n.raw_comment)
    print('result_type:', n.result_type.kind)
    print_type_info(n.result_type)
    print('mangled_name:', n.mangled_name)
    print('kind:', n.kind)
    print('lexical_parent:', n.lexical_parent)
    print('semantic_parent:', n.semantic_parent)
    print('linkage:', n.linkage)
    print('referenced:', n.referenced)
    cursor_bools(n)
    if n.referenced is not None:
        print('='*10)
        print_node_info(n.referenced)
        print('='*10)
    print_type_info(n.type)

def print_type_info(typ):
    print('-'*10, end='\n\t')
    print('type information:', end='\n\t')
    print("kind:", typ.kind.spelling, end='\n\t')
    print("spelling:", typ.spelling, end='\n\t')
    print("get_named_type():", typ.get_named_type().kind, end='\n\t')
    print("get_fields():", typ.get_fields(), end='\n\t')
    print("get_result():", typ.get_result().kind.spelling, end='\n\t')
    print("get_class_type():", typ.get_class_type(), end='\n\t')
    print("get_array_size():", typ.get_array_size(), end='\n\t')
    print('get_declaration():', typ.get_declaration())
    print('-'*10, end='\n\t')
    print()

'''Gets the sizeof(type) for any built-in C type.

Currently this works in the dirtiest way possible by compiling
and running a small C program.

This is VERY unsafe to use on arbitrary inputs because no attempt
at sanitation is made.
'''

from distutils import ccompiler
import tempfile
import subprocess
from pathlib import Path

def csizeof(typstr):
    '''Get the size in bytes of the C built-in type stated in the given string.

    Example: csizeof('sizeof(unsigned short int)') returns 2

    CAUTION: The input typestr will not be sanitized in any way. If you use
    this on untrusted input, it is at your own peril.
    '''
    print('typestr:',typstr)
    cc = ccompiler.new_compiler()
    with tempfile.TemporaryDirectory() as tmpdir:
        tdpath = Path(tmpdir)
        csource = tdpath / 'getsizeof.c'
        with open(csource, 'w') as csout:
            print(f'int main() {{ return {typstr}; }}', file=csout)
        objects = cc.compile([str(csource)], output_dir=str(tmpdir))
        exename = cc.executable_filename('getsizeof')
        cc.link_executable(objects=objects, output_progname=exename, output_dir=tmpdir)
        proc = subprocess.run([tdpath / exename])
    return proc.returncode
