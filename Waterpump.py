from __future__ import division, print_function;
import os
from solid import *
from solid.utils import *

lib = "C:/Users/Dylan/Documents/OpenSCAD/libraries/"

use(lib+"MCAD/2DShapes.scad")
use(lib+"testing.scad")

RESOLUTION = 0.1

#Set to 1 to see exploded model w/ all parts. Set to a higher value for more separation.
exploded = 0

#Set to True to see hollow parts cut in half.
cutaway = True

#Measurements for Outer Diameter and Wall Width are from standard North American Schedule charts.
#Body Measurements
schedule = 40

cylinderlength = 12

bushingspacer = 0.25

#Low Pressure Cylinder Specification
lpnom = 2
lpod = 2.375
lpww = 0.154

#High Pressure Cylinder Specification
hpnom = 1
hpod = 1.315
hpww = 0.133

#Internal Piston Measurements
mainpiston_rod_d = 0.25

#Hole Measurements
fittingdiameter = 0.5

#Spool Assembly Measurements
spoolinnernom = 1
spoolinnerod = 1.315
spoolinnerww = 0.133

spoolouternom = 1.25
spoolouterod = 1.660
spoolouterww = 0.140

"""---Utils---"""
### There is no "empty" OpenSCAD object, but to write the equivalent of
### OpenSCAD for loops in Python, you need one. The SolidPython examples
### assign an initial variable to a union() and add() to it. This alias
### is simply for clarity's sake.
def empty():
    return union()

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

"""---Mainbody---"""

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

def body():
    def lowpressurecylinder():
        @bom_part("2inx12in PVC Pipe", 8.18)
        def l_cylinder():
            return pipe(cylinderlength, lpod, lpww)

        @bom_part("2in PVC Cap", 1.22)
        def l_cap():
            return up(cylinderlength + exploded*2)(
                cap(lpod, lpww)
            )

        return up(bushingspacer/2 + exploded*3)(
            l_cylinder()
            +
            l_cap()
        )

    def highpressurecylinder():

        def h_cylinder():
            return pipe(cylinderlength, hpod, hpww)
            
        def h_cap():
            return up(cylinderlength + exploded*2)(
                cap(hpod, hpww)
                +
                up(exploded*3)(
                    cap(lpod,lpww)
                )
            )

        return mirror([0,0,1])(
            up(bushingspacer/2 + exploded*3)(
                h_cylinder()
                +
                h_cap()
            )
        )

    join = reducer(2.64, lpod, lpww, hpod, hpww, bushingspacer)

    plug = tube(0.5, hpod - hpww*2, mainpiston_rod_d, center=True)

    return lowpressurecylinder() + highpressurecylinder() + join + plug

"""---Mainpiston---"""

def mainpiston():
    r = mainpiston_rod_d/2

    return (
        cylinder(h = cylinderlength, r=r, center=True)
        +
        up(cylinderlength/2)(
            mirror([0,0,1])(
                piston(lpod - lpww*2, lpww, center=False)
            )
        )
        +
        down(cylinderlength/2)(
            piston(hpod - hpww*2, hpww, center=False)
        )
    )

"""---Hole-Drilling---"""

def fittings():
    return (
        # low-pressure end fitting
        up(cylinderlength)(
            fitting(lpww*4, fittingdiameter)
        )
        +
        # high-pressure end fitting
        down(cylinderlength)(
            fitting(lpww*4, fittingdiameter)
        )
        +
        # low pressure midpoint fitting
        translate([-lpod/2 + lpww, 0, lpww*4])(
            rotate([0,90,0])(
                fitting(lpww*5, fittingdiameter)
            )
        )
        +
        # high pressure midpoint fitting
        translate([-hpod/2 + hpww*0.5, 0, -hpww*4])(
            rotate([0,90,0])(
                fitting(lpww*4, fittingdiameter)
                +
                down(lpod/4)(
                    hull()(
                        fitting(lpww*4, fittingdiameter*2),
                        right(2)(
                            fitting(lpww*4, fittingdiameter*2)
                        )
                    )
                )
            )
        )
    )

"""---Spool Valves---"""

#Note: Only works for even-numbered counts.
#Unused, included as it was in the original .scad file
def cylinder_star(holewidth, diameter, count):
    out = empty()
    for i in range(0, count/2 + 1):
        out.add(
            rotate([0, 90, i*360/count])(
                cylinder(h = diameter*1.1, r = holewidth/2, center=True)
            )
        )

    return out 

def spool(length, od, ww, chambers, center=True):
    l = length - ww
    r = 0.1
    c = 0
    if center:
        c = -length/2

    def rods():
        out = empty()
        for i in range(0, 3):
            out.add(
                rotate([0, 0, i*120])(
                    right(od/4)(
                        cylinder(h = length, r = r)
                    )
                )
            )
        return out 

    def pistons():
        out = empty()
        for i in range(0, chambers + 1):
            out.add(
                up(i*l/chambers + ww/2)(
                    piston(od, ww)
                )
            )
        return out 

    if exploded == 0:
        out = rods() + pistons()
    else:
        out = up(exploded*(length + 1))(
            up(exploded*(length + 1))(
                rods() + pistons()
            )
            +
            rods()
        )
    return up(c)(
        out
    )

def five_valve(length, od, oww, id, iww, top=True, center=True, endpadding=0):

    def endports():
        return (
            up(length/2)(
                fitting(h = oww*4, d=fittingdiameter, center=True)
            )
            +
            down(length/2)(
                fitting(h = oww*4, d=fittingdiameter, center=True)
            )
        )

    def midports():
        def ports():
            out = empty()
            for i in range(-2, 3):
                j = 1
                if i % 2 == 0:
                    j = -1

                out.add(
                    translate([0, i*length/7, j*(od/2 - oww)])(
                        fitting(h = oww*3, d=fittingdiameter, center=True)
                    )
                )
            return out

        return rotate([90,0,0])(
            ports()
        )
    
    def _cutaway(do):
        if(do):
            return left(od/2)(
                cube([od, od*1.4, length*1.2 + endpadding*2], center=True)
            )
        else:
            return empty()

    # This block makes about as much sense as schnozzberries.
    ct = 0
    t = 0
    tn = 1
    if not top:
        ct = oww*2
        t = 1
        tn = -1

    c = 0
    if not center:
        c = length/2 + ct

    
    #(length*(1/7) and (1/14) reflects the length of the 3-chambered spool; at least this amount of
    #space is needed for the valve to fully actuate, so long as the input
    #and output adapters are flush with the inside of the valve. Endapdding
    #is an optional variable, in the event that the adapters are NOT flush.
    return up(c)(
        (
            pipe(length + endpadding*2, od, oww, center=True)
            +
            up(tn*length/2)(
                mirror([0,0,t])(
                    cap(od, oww)
                )
            )
            -
            endports()
            -
            midports()
            -
            _cutaway(cutaway)
        )
        +
        up(length*(1/14))(
            spool(length - length*(1/7), id, iww, 3, center=True)
        )
    )

"""---Assemblies---"""

def assembly():

    def _cutaway(do):
        offset = 5

        return forward(offset)(
            cube([cylinderlength*5, offset*2, offset*2], center=True)
        )
            
    # Main body and piston
    def mainbody():
        return (
            rotate([0, 90, 0])(
                body()
                -
                fittings()
            )
            -
            _cutaway(cutaway)
        )

    def five_valve_assembly(top=True):
        return five_valve(6, spoolouterod, spoolouterww, spoolinnerod, spoolinnerww, top=top, center=False)

    return (
        mainbody()  
        +
        rotate([0,90,0])(
            mainpiston()
        )
        +
        forward(6)(
            rotate([0,90,0])(
                five_valve_assembly()
                +
                down(6 + spoolouterww*2)(
                    five_valve_assembly(top=False)
                )
            )
        )
    )


if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'Waterpump.py.scad')

    scad_render_to_file(assembly(), file_out, file_header='$fs = %s;' % RESOLUTION)

# Hopefully merging into master?
