from sys import *
from helper_functions import *
memory_counter = 16
class Trigger:
    def __or__(self, a):
        return Pointer(a, 0, 1)

class Deref:
    def __init__(self, dorp, index=0):
        if isinstance(dorp, Deref):
            self.pointer = dorp.pointer + index
        else:
            self.pointer = dorp + index
    def get_value(self):
        return self.pointer.value
    def get_pointer(self):
        return self.pointer
    def __add__(self, a):
        return variable(self.value + a)
    def __radd__(self, a):
        return variable(self.value + a)
    def __int__(self):
        return self.value
    def __index__(self):
        return self.__int__()
    def __getitem__(self, i):
        return self.pointer[i]
    def __setitem__(self, i, a):
        self.pointer[i] = a
    #def __str__(self):
        #return "deref of: " + str(self.pointer)

    @property
    def value(self):
        return self.pointer.value

    @value.setter
    def value(self, val):
        self.pointer.value = val

class Pointer:
    def __init__(self, array, index, size, memory_loc=None):
        #print(array, index, size)
        global memory_counter
        self.str = False
        if isinstance(array, str):
            array = list(map(ord, array))
            array.append(0)
            self.str = True
        self.array = array
        self.index = index
        #print('index', index)
        #print('self.index', self.index)
        #print('self.array', self.array)
        self.size = size
        if not isinstance(self.array, list):
            self.array = [self.array]
        if memory_loc is None:
            self.memory_loc = memory_counter
            memory_counter += len(array)*size
        else:
            self.memory_loc = memory_loc

    @property
    def value(self):
        #print(self.array, self.index)
        if self.size == 1:
            #return ''.join(chr(x) for x in self.array[:len(self.array)])
            return ''.join(chr(x) for x in self.array[:self.array.index(0)])

        return self.array[self.index]
    @value.setter
    def value(self, val):
        self.array[self.index] = val

    def __add__(self, a):
        #print(a, self.index)
        #print(self.array)
        return Pointer(self.array, self.index + a, self.size, self.memory_loc)
    def __get__(self, n):
        return self.array[self.index+n]
    def __getitem__(self, i):
        return self.array[i]
    def __setitem__(self, i, a):
        #print(self.array)
        self.array[i] = a
    def __str__(self):
        if self.size == 1:
            try:
                null_byte = self.array.index(0)
            except ValueError:
                raise ValueError("No null byte in string") from None
            return ''.join(chr(x) for x in self.array[:null_byte])
        else:
            return str(self.array)+ " " + str(self.index) + " " + str(self.size)
            #raise NotImplementedError("need pointer alias for string conversion")

    def __int__(self):
        return self.memory_loc + self.index * self.size
    def __index__(self):
        return self.__int__()

class Pointer_alias:
    def __init__(self, dorp, a_size, index=-1):
        if isinstance(dorp, Deref):
            self.pointer = dorp.pointer
        else:
            self.pointer = dorp
        self.a_size = a_size
        if index == -1:
            self.index = self.pointer.index * self.pointer.size // a_size
        else:
            self.index = index
    def __str__(self):
        return "index: " + str(self.index) + " a_size: " + str(self.a_size) + " data: " + ' '.join([str(i) for i in self.pointer.array])

    @property
    def value(self):
        #print('in p alias', self.pointer.array, self.index, self.a_size)
        return self[self.index]
    @value.setter
    def value(self, val):
        self[self.index] = val

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
            # print(oi, of)
            # of = self.pointer.size - (i % self.pointer.size + 1) * self.a_size
            # print(self.pointer[oi]) 
            # print(of)
            bmask = (1 << self.pointer.size*8) - 1
            lmask = (1 << self.a_size*8) - 1
            shift_amt = of*self.a_size*8
            lmask <<= shift_amt
            mask = bmask^lmask
            # bin(mask)
            self.pointer[oi] &= mask
            self.pointer[oi] ^= j << shift_amt
        elif self.a_size > self.pointer.size:
            pass

    def __int__(self):
        return self.pointer.memory_loc
    def __index__(self):
        return self.pointer.memory_loc
    def __add__(self, a):
        return Pointer_alias(self.pointer, self.a_size, self.index + a)

def variable(a, index=0, size=1):
    #print(a, index, size)
    if not isinstance(a, list):
        return Deref(Pointer([a], 0, size), index)
    else:
        return Deref(Pointer(a, 0, size), index)
