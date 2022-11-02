from sys import *
from helper_functions import *
memory_counter = 16
class Pointer:
    def __init__(self, array, index, size, memory_loc=None):
        global memory_counter
        if isinstance(array, str):
            array = list(array)
            array.append('\x00')
        self.array = array
        self.index = index
        self.size = size

        if memory_loc is None:
            self.memory_loc = memory_counter
            memory_counter += len(array)*size
        else:
            self.memory_loc = memory_loc

    def deref(self):
        return self.array[self.index]
    def getsize(self):
        return self.size
    def __add__(self, a):
        return Pointer(self.array, self.index + a, self.memory_loc)
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
        ret = ""
        for i in self.array:
            if i == '\x00':
                return ret
            ret += chr(i)
        #return ret + '\x00'
        return ret

    def __int__(self):
        return self.memory_loc + self.index * self.size
    def __index__(self):
        return self.__int__()

class Pointer_alias:
    def __init__(self, pointer, a_size):
        self.pointer = pointer
        self.a_size = a_size
        self.index = self.pointer.index * pointer.size // a_size
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
            oi, of = divmod(i, self.pointer.size // self.a_size)
            print(oi, of)
            #of = self.pointer.size - (i % self.pointer.size + 1) * self.a_size
            print(self.pointer[oi]) 
            print(of)
            bmask = (1 << self.pointer.size*8) - 1
            lmask = (1 << self.a_size*8) - 1
            shift_amt = of*self.a_size*8
            lmask <<= shift_amt
            mask = bmask^lmask
            bin(mask)
            self.pointer[oi] &= mask
            self.pointer[oi] ^= j << shift_amt
        elif self.a_size > self.pointer.size:
            pass
    # UPDATE THIS
    def __setattr__(self, name, value):
        if name == 'value':
            self.pointer.array[self.index] = value
        else:
            super().__setattr__(name, value)
    def __getattr__(self, name):
        if name == 'value':
            return self.pointer.array[self.index]
        else:
            super().__getattr__(name)
    def __int__(self):
        return self.pointer.memory_loc
    def __index__(self):
        return self.pointer.memory_loc
