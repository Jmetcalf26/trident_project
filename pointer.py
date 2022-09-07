class Pointer:
    def __init__(self, array, index):
        self.array = array
        self.index = index
    def get():
        return self.array[self.index]
    def __add__(self, a):
        return self.index + a

