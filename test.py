#!/usr/bin/env python3

from ansipy import *

a = ColoredStr('hello world')
b = ColoredStr('asdf')

a.color = 'R'
b.color = 'G'

print(a + b)

