from ast import *
print(dump(parse(open('simple.py').read()), indent=3))
