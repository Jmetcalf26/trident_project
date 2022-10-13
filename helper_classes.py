from sys import *

class Pointer:
    def __init__(self, array, index, size):
        self.array = array
        self.index = index
        self.size = size
    def deref(self):
        return self.array[self.index]
    def getsize(self):
        return self.size
    def __add__(self, a):
        return Pointer(self.array, self.index + a)
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
        return "index: " + str(self.index) + " size: " + str(self.size) + " data: " + ' '.join([str(i) for i in self.array])


class Pointer_alias:
    def __init__(self, pointer, a_size):
        self.pointer = pointer
        self.a_size = a_size
        self.index = self.pointer.index
    def __str__(self):
        return "index: " + str(self.index) + " a_size: " + str(self.a_size) + " data: " + ' '.join([str(i) for i in self.pointer.array])
