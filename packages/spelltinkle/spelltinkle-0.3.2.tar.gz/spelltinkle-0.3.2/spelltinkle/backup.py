import difflib
t1 = ['asdgf', 'gggggggg', 'ggg', 'hhh']
t2 = list(t1)
del t2[2]
print('\n'.join(difflib.unified_diff(t1, t2, lineterm='', n=1)))
# Respect file permissions .... (secrets.py)
