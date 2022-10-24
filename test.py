from helper_classes import *

a = Pointer([0x41424344, 0x45464748], 0, 4)
b = Pointer_alias(a, 2)
print("orig: 4. alias: 2.")
for i in range(4):
        print(i, hex(b[i]))
c = Pointer_alias(a, 1)

print("orig: 4. alias: 1.")
for i in range(8):
        print(i, hex(c[i]))

a = Pointer([0x4142, 0x4344, 0x4546, 0x4748], 0, 2)
b = Pointer_alias(a, 1)
print("orig: 2. alias: 1.")
for i in range(8):
        print(i, hex(b[i]))

a = Pointer([0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48], 0, 1)
b = Pointer_alias(a, 4)
print("orig: 1. alias: 4.")
for i in range(2):
        print(i, hex(b[i]))

a = Pointer([0x4142, 0x4344, 0x4546, 0x4748], 0, 2)
b = Pointer_alias(a, 4)
print("orig: 2. alias: 4.")
for i in range(2):
        print(i, hex(b[i]))
print(hex(a[0] + (a[1] << 16)))
