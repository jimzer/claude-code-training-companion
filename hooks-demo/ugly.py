import os, sys, json
import collections
from typing import List, Dict, Optional

x = 1
y = 2
z = x + y


def ugly_function(a, b, c):
    result = a + b + c
    unused_var = "never used"
    if result > 10:
        print("big")
    elif result > 5:
        print("medium")
    else:
        print("small")
    return result


class ugly_class:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def do_something(self):
        l = [1, 2, 3, 4, 5]
        d = {"a": 1, "b": 2, "c": 3}
        for i in l:
            if i == 3:
                pass
            else:
                print(i)
        return l


result = ugly_function(1, 2, 3)
obj = ugly_class("test", 42)
