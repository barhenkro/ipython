# coding: utf-8

# This script autogenerates `IPython.core.latex_symbols.py`, which contains a
# single dict , named `latex_symbols`. The keys in this dict are latex symbols,
# such as `\\alpha` and the values in the dict are the unicode equivalents for
# those. Most importantly, only unicode symbols that are valid identifers in
# Python 3 are included. 

# 
# The original mapping of latex symbols to unicode comes from the `latex_symbols.jl` files from Julia.

from __future__ import print_function

# Import the Julia LaTeX symbols
print('Importing latex_symbols.js from Julia...')
import requests
url = 'https://raw.githubusercontent.com/JuliaLang/julia/master/base/latex_symbols.jl'
r = requests.get(url)


# Build a list of key, value pairs
print('Building a list of (latex, unicode) key-vaule pairs...')
lines = r.text.splitlines()[60:]
lines = [line for line in lines if '=>' in line]
lines = [line.replace('=>',':') for line in lines]

def line_to_tuple(line):
    """Convert a single line of the .jl file to a 2-tuple of strings like ("\\alpha", "α")"""
    kv = line.split(',')[0].split(':')
#     kv = tuple(line.strip(', ').split(':'))
    k, v = kv[0].strip(' "'), kv[1].strip(' "')
#     if not test_ident(v):
#         print(line)
    return k, v

assert line_to_tuple('    "\\sqrt" : "\u221A",') == ('\\sqrt', '\u221A')
lines = [line_to_tuple(line) for line in lines]


# Filter out non-valid identifiers
print('Filtering out characters that are not valid Python 3 identifiers')

def test_ident(i):
    """Is the unicode string a valid Python 3 identifer."""
    try:
        exec('a%s = 10' % i, {}, {})
    except SyntaxError:
        return False
    else:
        return True

assert test_ident("α")
assert not test_ident('‴')

valid_idents = [line for line in lines if test_ident(line[1])]


# Write the `latex_symbols.py` module in the cwd

s = """# encoding: utf-8

# This file is autogenerated from the file:
# https://raw.githubusercontent.com/JuliaLang/julia/master/base/latex_symbols.jl
# This original list is filtered to remove any unicode characters that are not valid
# Python identifiers.

latex_symbols = {\n
"""
for line in valid_idents:
    s += '    "%s" : "%s",\n' % (line[0], line[1])
s += "}\n"

with open('latex_symbols.py', 'w', encoding='utf-8') as f:
    f.write(s)


