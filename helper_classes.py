from sys import *

class Pointer:
    def __init__(self, array, index):
        self.array = array
        self.index = index
    def deref(self):
        return self.array[self.index]
    def __add__(self, a):
        return Pointer(self.array, self.index + a)
    def __get__(self, n):
        return self.array[self.index+n]

class array:
    def __init__(self, arr, size):
        self.arr = arr
        self.size = size
    def __getitem__(self, i):
        return self.arr[i]
    def __str__(self):
        return "size: " + str(self.size) + " data: " + ' '.join([str(i) for i in self.arr])
