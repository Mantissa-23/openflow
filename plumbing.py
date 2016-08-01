from __future__ import division, print_function;
from solid import *
from solid.utils import *

lib = "C:/Users/Dylan/Documents/OpenSCAD/libraries/"

use(lib+"MCAD/2DShapes.scad")

"""---General Plumbing---"""

def tube(h, od, id, center=False):
    return cylinder(h = h, r = od/2, center = center) - cylinder(h = h, r = id/2, center = center)

def pipe(h, od, ww, center=False):
    return tube(h = h, od = od, id = od-ww*2, center = center)

def cap(od, ww):
    ro = od/2 + ww
    ri = od/2
    cap = up(-ri)(
        linear_extrude(ro)(
            ngon(6, ro*1.1)
        )
        -
        cylinder(h = ri, r = ri)
    )
    return cap

# Add threads at some point?
def fitting(h, d, center=True):
    return cylinder(h=h, r=d/2, center=center)

def piston(od, ww, center=True):
    r = od/2 - ww;
    c = 0

    if not center:
        c = ww/3

    p = (
        pipe(ww, od, ww, center=center)
        +
        up(c)(cylinder(h=ww/3, r=r, center=center))
    )

    return p

# Refactor this shit
def reducer(length, largeod, largeww, smallod, smallww, separatorwidth):
    od = largeod + largeww*2
    sod = smallod + smallww*2
    
    large = cylinder(h = length, r = od/2, center=True)

    twoin = up(separatorwidth/2)(
        cylinder(h = length, r = largeod/2)
    )

    onein = down(separatorwidth/2)(
        mirror([0,0,1])(
            cylinder(h = length, r = smallod/2)
        )
        +
        cylinder(h = length, r = (smallod - smallww*2)/2, center=True)
        +
        mirror([0,0,1])(
            pipe(length, largeod, (largeod-sod)/2)
        )
    )

    adapters = large - (
        twoin
        +
        onein
    )

    for i in range(0,4):
        adapters = adapters + rotate([0, 0, i*90 + 45])(
            translate([0, (largeod+sod)/4, -length/4])(
                cube([separatorwidth/2, (largeod - sod)/2 + 0.1, length/2], center=True)
            )
        )

    return adapters
