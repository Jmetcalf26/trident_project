from helper_classes import *

a = Pointer([0x11223344, 0x55667788], 0, 4)
print("a = Pointer([0x11223344, 0x55667788], 0, 4)")
b = Pointer_alias(a, 2)
print("orig: 4. alias: 2.")
for i in range(4):
        print(i, hex(b[i]))
c = Pointer_alias(a, 1)

print("orig: 4. alias: 1.")
for i in range(8):
        print(i, hex(c[i]))

print("a = Pointer([0x1122, 0x3344, 0x5566, 0x7788], 0, 2)")
a = Pointer([0x1122, 0x3344, 0x5566, 0x7788], 0, 2)
b = Pointer_alias(a, 1)
print("orig: 2. alias: 1.")
for i in range(8):
        print(i, hex(b[i]))

a = Pointer([0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88], 0, 1)
print("a = Pointer([0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88], 0, 1)")
b = Pointer_alias(a, 4)
print("orig: 1. alias: 4.")
for i in range(2):
        print(i, hex(b[i]))

a = Pointer([0x1122, 0x3344, 0x5566, 0x7788], 0, 2)
print("a = Pointer([0x1122, 0x3344, 0x5566, 0x7788], 0, 2)")
b = Pointer_alias(a, 4)
print("orig: 2. alias: 4.")
for i in range(2):
        print(i, hex(b[i]))
print(hex(a[0] + (a[1] << 16)))

a = Pointer([0x4142, 0x4344, 0x4546, 0x4748], 0, 2)
b = Pointer_alias(a, 2)
print("orig: 2. alias: 2.")
for i in range(4):
        print(i, hex(b[i]))
print(hex(a[0] + (a[1] << 16)))

a = Pointer([0x41424344, 0x45464748], 0, 4)
b = Pointer_alias(a, 2)
print("orig: 4. alias: 2.")
for i in range(4):
        print(i, hex(b[i]))

print("b[0] = 0x494a")
b[0] = 0x494a
print("orig: 4. alias: 2.")
for i in range(4):
        print(i, hex(b[i]))
for i in range(2):
        print(i, hex(a[i]))

print("b[1] = 0x4b4c")
b[1] = 0x4b4c
print("orig: 4. alias: 2.")
for i in range(4):
        print(i, hex(b[i]))
for i in range(2):
        print(i, hex(a[i]))
print("b[2] = 0x4d4e")
b[2] = 0x4d4e
print("orig: 4. alias: 2.")
for i in range(4):
        print(i, hex(b[i]))
for i in range(2):
        print(i, hex(a[i]))

