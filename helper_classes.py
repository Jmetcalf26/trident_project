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
    def __str__(self):
        return "index: " + str(self.index) + "size: " + str(self.size) + " data: " + ' '.join([str(i) for i in self.arr])


# class Data:
#     def __init__(self, value, size):
#         self.value = value
#         self.size = size
#     def __add__(self, a):
#         return  

class array:
    def __init__(self, arr, size):
        self.arr = arr
        self.size = size
    def __getitem__(self, i):
        return self.arr[i]
    def __str__(self):
        return "size: " + str(self.size) + " data: " + ' '.join([str(i) for i in self.arr])
