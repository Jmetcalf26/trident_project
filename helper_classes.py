from sys import *
from helper_functions import *

class Pointer:
    def __init__(self, array, index, size):
        self.array = array
        if isinstance(array, str):
            self.array = [ord(c) for c in array] + [0]
        self.index = index
        self.size = size
    def deref(self):
        return self.array[self.index]
    def getsize(self):
        return self.size
    def __add__(self, a):
        return Pointer(self.array, self.index + a, self.size)
    def __get__(self, n):
        return self.array[self.index+n]
    def __getitem__(self, i):
        return self.array[i]
    def __setitem__(self, i, a):
        self.array[i] = a
    def __setattr__(self, name, value):
        if name == 'value':
            self.array[self.index] = value
        else:
            super().__setattr__(name, value)
    def __getattr__(self, name):
        if name == 'value':
            return self.array[self.index]
        else:
            super().__getattr__(name)
    def __str__(self):
        if self.size == 1:
            try:
                null_byte = self.array.index(0)
            except ValueError:
                raise ValueError("No null byte in string") from None
            return ''.join(chr(x) for x in self.array[:null_byte])
        else:
            raise NotImplementedError("need pointer alias for string conversion")
        #return "index: " + str(self.index) + " size: " + str(self.size) + " data: " + ' '.join([str(i) for i in self.array])


class Pointer_alias:
    def __init__(self, pointer, a_size):
        self.pointer = pointer
        self.a_size = a_size
        self.index = self.pointer.index
    def __str__(self):
        return "index: " + str(self.index) + " a_size: " + str(self.a_size) + " data: " + ' '.join([str(i) for i in self.pointer.array])

    def __getitem__(self, i):
        if self.a_size < self.pointer.size:
            if self.a_size == 1:
                oi = i // self.pointer.size
                of = i % self.pointer.size
            else:
                oi = i // self.a_size
                of = i %  self.a_size
            mask = (1 << 8*self.a_size) - 1
            #print(bin(mask))
            #print(hex(self.pointer.array[oi]))
            #print(of * 8 * self.a_size)
            value = (self.pointer[oi] >> (of * 8 * self.a_size)) & mask
            return value
        elif self.a_size > self.pointer.size:
            value = 0
            size_diff = self.a_size // self.pointer.size
            for j in range(size_diff):
                shift = 8 * j * self.pointer.size 
                index = j + (i * size_diff)
                value += self.pointer[index] << shift
            return value
        else:
            return self.pointer[i]
    def __setitem__(self, i, j):
        if self.a_size < self.pointer.size:
            oi = i // self.pointer.size
            print(oi)
            of = self.pointer.size - (i % self.pointer.size + 1) * self.a_size
            print(of)
            mask = (1 << self.pointer.size*8) - 1
            bin(mask)
            mask ^= ((1<<(self.pointer.size-of)*8)-1)
            bin(mask)
            self.pointer[oi] &= mask
            self.pointer[oi] += j << (oi)*8
