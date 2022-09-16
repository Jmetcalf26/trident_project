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

