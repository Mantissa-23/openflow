/*----------------------------------------------------------------------
OpenFlow, an open source, gravitational pressure-driven hydraulic pump.
--------------------------------------------------------------------*/

use <MCAD/2DShapes.scad>;
use <testing.scad>;

//Inches are fairly small units for OpenSCAD; increase resolution of geometry
//to make the model easier to view.
$fs = 0.1;

//Set to 1 to see exploded model w/ all parts. Set to a higher value for more separation.
exploded = 0;

cutaway = true;

//Measurements for Outer Diameter and Wall Width are from standard North American Schedule charts.
//Body Measurements
schedule = 40;

cylinderlength = 12;

//Low Pressure Cylinder Specification
lpnom = 2;
lpod = 2.375;
lpww = 0.154;

//High Pressure Cylinder Specification
hpnom = 1;
hpod = 1.315;
hpww = 0.133;

//Internal Piston Measurements
mainpiston_rod_d = 0.25;

//Hole Measurements
holediameter = 0.5;

//Spool Assembly Measurements
spoolinnernom = 1;
spoolinnerod = 1.315;
spoolinnerww = 0.133;

spoolouternom = 1.25;
spoolouterod = 1.660;
spoolouterww = 0.140;

/*----------------------
----General Plumbing---
--------------------*/

module pipe(height, outerdiameter, wallthickness, center=false) {
	difference() {
		ro = outerdiameter/2;
		ri = outerdiameter/2 - wallthickness;
		cylinder(h = height, r1 = ro, r2 = ro, center=center);
		cylinder(h = height, r1 = ri, r2 = ri, center=center);
	}
}

module tube(height, outerdiameter, innerdiameter, center=false) {
	difference() {
		ro = outerdiameter/2;
		ri = innerdiameter/2;
		cylinder(h = height, r1 = ro, r2 = ro, center=center);
		cylinder(h = height, r1 = ri, r2 = ri, center=center);
	}
}

module cap(outerdiameter, wallthickness) {
	ro = outerdiameter/2+wallthickness;
	ri = outerdiameter/2;
	translate([0,0,-ri])
		difference() {
			linear_extrude(ro)
				ngon(6, ro*1.1);
			cylinder(h = ri, r1 = ri, r2 = ri);
		}
}

//Add threads?
module hole(h, d, center=true) {
	cylinder(h=h, r1=d/2, r2=d/2, center=center);
}

module piston(outerdiameter, wallthickness, center=true) {
	r = outerdiameter/2 - wallthickness;
	c = center ? 0 : wallthickness/3;
	union() {
		pipe(wallthickness, outerdiameter, wallthickness, center=center);
		translate([0,0,c])
		cylinder(h=wallthickness/3, r1=r, r2=r, center=center);
	}
}

/*---------------
----Main Body---
-------------*/

module reducer(length, lad, laww, sad, saww, separatorwidth) {
	od = lad+laww*2;

	sod = sad+saww*2;
	union() {
		difference() {
			//Large initial cylinder
			cylinder(h = length, r1 = od/2, r2 = od/2, center=true);
			//2" adapter
			translate([0,0,separatorwidth/2]) {
				cylinder(h = length, r1 = lpod/2, r2 = lpod/2);
			}
			translate([0,0,-separatorwidth/2]) {
				//1" adapter
				mirror([0,0,1]) {
					cylinder(h = length, r1 = hpod/2, r2=hpod/2);
				}
				cylinder(h = length, r1 = (hpod - hpww*2)/2, r2 = (hpod-hpww*2)/2, center=true);
				//Spoke support section
				mirror([0,0,1]) {
					pipe(length, lpod, (lpod-sod)/2);
				}
			}
		}
		//Add spokes
		for(i = [0:3]) {
			rotate([0,0,i*90 + 45]) {
				translate([0,(lpod+sod)/4,-length/4]) {
					cube([separatorwidth/2, (lpod-sod)/2 + 0.1, length/2], center=true);
				}
			}
		}
	}
}

module body() {
	bushingspacer = 0.25;

	//Low-Pressure Cylinder
	translate([0, 0, bushingspacer/2 + exploded*3]) {
		pipe(cylinderlength, lpod, lpww);
		translate([0, 0, cylinderlength + exploded*2])
			cap(lpod, lpww);
	}

	//High-Pressure Cylinder
	mirror([0,0,1]) {
		translate([0, 0, bushingspacer/2 + exploded*3]) {
			pipe(cylinderlength, hpod, hpww);
			translate([0,0,cylinderlength + exploded*2]) {
				cap(hpod, hpww);
				translate([0,0,exploded*3])
					cap(lpod, lpww);
			}
		}
	}

	//Connecting Bushing
	reducer(2.64, lpod, lpww, hpod, hpww, bushingspacer);

	//Internal Plug
	tube(0.5, hpod - hpww*2, mainpiston_rod_d, center=true);
}

/*-----------------
----mainpiston----
---------------*/

module mainpiston() {
	r = mainpiston_rod_d/2;
	union() {
		cylinder(h = cylinderlength, r1=r, r2=r, center=true);
		{
		translate([0,0,cylinderlength/2])
			mirror([0,0,1])
				piston(lpod - lpww*2, lpww, center=false);
		translate([0,0,-cylinderlength/2])
			piston(hpod - hpww*2, hpww, center=false);
		}
	}
}

/*-------------------------
----Drill holes in body---
-----------------------*/

module holes() {
	translate([cylinderlength, 0, 0]) {
		rotate([0,90,0])
			hole(lpww*4, holediameter);
	}
	translate([-cylinderlength, 0, 0]) {
		rotate([0,90,0])
			hole(lpww*4, holediameter);

	}
	translate([lpww*4, 0, lpod/2 + lpww])
		hole(lpww*5, holediameter);
	translate([-hpww*4, 0, (hpod + lpod)/4 + lpww])
		hole(lpww*10, holediameter);
}

/*-------------------
----Spool Valves----
-----------------*/

//Note: Only works for even-numbered counts.
//Unused.
module cylinder_star(holewidth, diameter, count) {
	union() {
		for(i = [0:count/2]) {
			rotate([0, 90, i*360/count])
				cylinder(h = diameter*1.1, r1 = holewidth/2, r2 = holewidth/2, center=true);
		}
	}
}

module spool(length, outerdiameter, wallwidth, chambers, center=true) {
	l = length - wallwidth;
	r = 0.1;
	c = center ? -length/2 : 0;

	module rods() {
		for(i=[0:2]) {
			rotate([0,0,i*120])
				translate([outerdiameter/4, 0, 0])
				cylinder(h=length, r1=r, r2=r);
		}
	}

	translate([0,0,c]) {
		if(exploded==0) {
			union() {
				for(i = [0:chambers]) {
					translate([0,0,i*l/chambers + wallwidth/2])
						piston(outerdiameter, wallwidth);
				}
				rods();
			}
		}
		else {
			translate([0,0,exploded*(length + 1)]) {
				translate([0,0,exploded*(length + 1)]) {
					difference() {
						for(i = [0:chambers]) {
							translate([0,0,i*l/(chambers*2) + wallwidth/2])
								piston(outerdiameter, wallwidth);
						}
						rods();
					}
				}
				rods();
			}
		}
	}
}

module five_valve(length, outerdiameter, outerww, innerdiameter, innerww, center=true, endpadding=0) {
	module valves() {
		rotate([90,0,0]) {
			for(i = [-2:2]) {
				//Alternates holes between one side and the other.
				j = i % 2 == 0 ? -1 : 1;
				translate([0, i*length/7, j*(outerdiameter/2 - outerww)])
					hole(h = outerww*3, d=holediameter, center=true);
			}
		}
		translate([0,0,length/2])
			hole(h = outerww*4, d=holediameter, center=true);
		translate([0,0,-length/2])
			hole(h = outerww*4, d=holediameter, center=true);
	}

	c = center ? 0 : length/2 + outerww;
	//(length*(1/7) and (1/14) reflects the length of the 3-chambered spool; at least this amount of
	//space is needed for the valve to fully actuate, so long as the input
	//and output adapters are flush with the inside of the valve. Endapdding
	//is an optional variable, in the event that the adapters are NOT flush.
	translate([0,0,c]) {
		translate([0,0,length*(1/14)])
			spool(length - length*(1/7), innerdiameter, innerww, 3, center=true);
		difference() {
			difference() {
				union() {
					pipe(length + endpadding*2, outerdiameter, outerww, center=true);
					translate([0,0,length/2])
						cap(outerdiameter, outerww);
					translate([0,0,-length/2])
						mirror([0,0,1])
							cap(outerdiameter, outerww);
				}
				valves();
			}
			if(cutaway) {
				translate([-outerdiameter/2, 0, 0])
					cube([outerdiameter, outerdiameter*1.4, length*1.2 + endpadding*2], center=true);
			}
		}
	}
}


module spools() {
	
}

/*------------------
----Final Object---
----------------*/

module assembly() {
	//Main body and piston
	difference() {
		difference() {
			rotate([0, 90, 0]) {
				body();
			}
			holes();
		}
		if(cutaway) {
			offset = 5;
			translate([0, offset, 0])
				cube([cylinderlength*5, offset*2, offset*2], center=true);
		}
	}
	rotate([0,90,0])
		mainpiston();

	//Spool Valves
	module five_valve_assembly() {
		five_valve(6, spoolouterod, spoolouterww, spoolinnerod, spoolinnerww, center=false);
	}

	translate([0, 6, 0]) {
		rotate([0,90,0]) {
			five_valve_assembly();
			translate([0,0,-(6 + spoolouterww*2)])
				five_valve_assembly();
		}
	}
}

//test_overlap()
assembly();