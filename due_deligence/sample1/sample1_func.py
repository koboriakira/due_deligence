import sys
import os

print(os.getcwd())
sys.path.append(os.getcwd())
print(sys.path)

from sample2 import sample2_func
sample2_func.func()
