from solid import union

"""---Utils---"""
### For clarity when building OpenSCAD objects via for loops. Pythonically,
### adding onto a union() object makes sense, but it isn't very OpenSCAD-ic.
def empty():
    return union()
