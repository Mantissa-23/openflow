$fs = 0.1;use <C:/Users/Dylan/Documents/OpenSCAD/libraries/MCAD/2DShapes.scad>


difference() {
	union() {
		union() {
			union() {
				translate(v = [0, 0, 0.1250000000]) {
					union() {
						difference() {
							cylinder(h = 12, r = 1.1875000000, center = false);
							cylinder(h = 12, r = 1.0335000000, center = false);
						}
						translate(v = [0, 0, 12]) {
							translate(v = [0, 0, -1.1875000000]) {
								difference() {
									linear_extrude(height = 1.3415000000) {
										ngon(radius = 1.4756500000, sides = 6);
									}
									cylinder(h = 1.1875000000, r = 1.1875000000);
								}
							}
						}
					}
				}
				mirror(v = [0, 0, 1]) {
					translate(v = [0, 0, 0.1250000000]) {
						union() {
							difference() {
								cylinder(h = 12, r = 0.6575000000, center = false);
								cylinder(h = 12, r = 0.5245000000, center = false);
							}
							translate(v = [0, 0, 12]) {
								union() {
									translate(v = [0, 0, -0.6575000000]) {
										difference() {
											linear_extrude(height = 0.7905000000) {
												ngon(radius = 0.8695500000, sides = 6);
											}
											cylinder(h = 0.6575000000, r = 0.6575000000);
										}
									}
									translate(v = [0, 0, 0]) {
										translate(v = [0, 0, -1.1875000000]) {
											difference() {
												linear_extrude(height = 1.3415000000) {
													ngon(radius = 1.4756500000, sides = 6);
												}
												cylinder(h = 1.1875000000, r = 1.1875000000);
											}
										}
									}
								}
							}
						}
					}
				}
			}
			union() {
				union() {
					union() {
						union() {
							difference() {
								cylinder(h = 2.6400000000, r = 1.3415000000, center = true);
								union() {
									translate(v = [0, 0, 0.1250000000]) {
										cylinder(h = 2.6400000000, r = 1.1875000000);
									}
									translate(v = [0, 0, -0.1250000000]) {
										union() {
											union() {
												mirror(v = [0, 0, 1]) {
													cylinder(h = 2.6400000000, r = 0.6575000000);
												}
												cylinder(h = 2.6400000000, r = 0.5245000000, center = true);
											}
											mirror(v = [0, 0, 1]) {
												difference() {
													cylinder(h = 2.6400000000, r = 1.1875000000, center = false);
													cylinder(h = 2.6400000000, r = 0.7905000000, center = false);
												}
											}
										}
									}
								}
							}
							rotate(a = [0, 0, 45]) {
								translate(v = [0, 0.9890000000, -0.6600000000]) {
									cube(center = true, size = [0.1250000000, 0.4970000000, 1.3200000000]);
								}
							}
						}
						rotate(a = [0, 0, 135]) {
							translate(v = [0, 0.9890000000, -0.6600000000]) {
								cube(center = true, size = [0.1250000000, 0.4970000000, 1.3200000000]);
							}
						}
					}
					rotate(a = [0, 0, 225]) {
						translate(v = [0, 0.9890000000, -0.6600000000]) {
							cube(center = true, size = [0.1250000000, 0.4970000000, 1.3200000000]);
						}
					}
				}
				rotate(a = [0, 0, 315]) {
					translate(v = [0, 0.9890000000, -0.6600000000]) {
						cube(center = true, size = [0.1250000000, 0.4970000000, 1.3200000000]);
					}
				}
			}
		}
		difference() {
			cylinder(h = 0.5000000000, r = 0.5245000000, center = true);
			cylinder(h = 0.5000000000, r = 0.1250000000, center = true);
		}
	}
	union() {
		union() {
			union() {
				translate(v = [0, 0, 12]) {
					cylinder(h = 0.6160000000, r = 0.2500000000, center = true);
				}
				translate(v = [0, 0, -12]) {
					cylinder(h = 0.6160000000, r = 0.2500000000, center = true);
				}
			}
			translate(v = [1.3415000000, 0, 0.6160000000]) {
				rotate(a = [0, 90, 0]) {
					cylinder(h = 0.7700000000, r = 0.2500000000, center = true);
				}
			}
		}
		translate(v = [0.7240000000, 0, -0.5320000000]) {
			rotate(a = [0, 90, 0]) {
				union() {
					cylinder(h = 0.6160000000, r = 0.2500000000, center = true);
					translate(v = [0, 0, 0.5937500000]) {
						hull() {
							cylinder(h = 0.6160000000, r = 0.5000000000, center = true);
							translate(v = [2, 0, 0]) {
								cylinder(h = 0.6160000000, r = 0.5000000000, center = true);
							}
						}
					}
				}
			}
		}
	}
}
/***********************************************
******      SolidPython code:      *************
************************************************
 
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
    lowpressurec = up(bushingspacer/2 + exploded*3)(
        pipe(cylinderlength, lpod, lpww)
        +
        up(cylinderlength + exploded*2)(
            cap(lpod, lpww)
        )
    )

    highpressurec = mirror([0,0,1])(
        up(bushingspacer/2 + exploded*3)(
            pipe(cylinderlength, hpod, hpww)
            +
            up(cylinderlength + exploded*2)(
                cap(hpod, hpww)
                +
                up(exploded*3)(
                    cap(lpod,lpww)
                )
            )
        )
    )

    join = reducer(2.64, lpod, lpww, hpod, hpww, bushingspacer)

    plug = tube(0.5, hpod - hpww*2, mainpiston_rod_d, center=True)

    return lowpressurec + highpressurec + join + plug

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

def holes():
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
        translate([lpod/2 + lpww, 0, lpww*4])(
            rotate([0,90,0])(
                fitting(lpww*5, fittingdiameter)
            )
        )
        +
        # high pressure midpoint fitting
        translate([hpod/2 + hpww*0.5, 0, -hpww*4])(
            rotate([0,90,0])(
                fitting(lpww*4, fittingdiameter)
                +
                up(lpod/4)(
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

"""---Assemblies---"""

def assembly():
    b = body()
    h = holes()
    return b - h

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'Waterpump.py.scad')

    scad_render_to_file(assembly(), file_out, file_header='$fs = %s;' % RESOLUTION)
 
 
***********************************************/
                            
