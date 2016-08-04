from __future__ import division, print_function;
from solid import *
from solid.utils import *
import renderer

from utils import *
from plumbing import *

"""---Plumbing---"""
class body:
    lpod

    def __init__(self, lpod, lpww, hpod, hpww, bushingspacer, exploded, cutaway, ):
        lpod = 
    def cylinders(self):
        @bom_part("2in PVC Cap", 1.22, link="http://www.homedepot.com/p/2-in-x-10-ft-PVC-Sch-40-Plain-End-Pipe-531137/100161954", use="Removable cover for LPC", leftover=0)
        def cap_2in():
            return cap(lpod, lpww)

        # Add actual geometry for this instead of just throwing it all into one big placeholder part
        @bom_part("2in PVC SxFPT Adapter", 1.53, link="http://www.homedepot.com/p/Charlotte-Pipe-2-in-PVC-Sch-40-Female-S-x-FPT-Adapter-PVC021011600HD/203811416", use="Connects LPC to Reducer Bushing", leftover=0)
        @bom_part("2inx10' PVC Pipe", 8.18, link="http://www.homedepot.com/p/2-in-x-10-ft-PVC-Sch-40-Plain-End-Pipe-531137/100161954", use="LPC, Low-Pressure Cylinder", leftover="9'")
        def pipe_2inx1ft():
            return pipe(cylinderlength, lpod, lpww)

        def lowpressurecylinder():
            return up(bushingspacer/2 + exploded*3)(
                pipe_2inx1ft()
                +
                up(cylinderlength + exploded*2)(
                    cap_2in()
                )
            )

        @bom_part()
        @bom_part("1in PVC Cap", 1.32, link="http://www.homedepot.com/p/Charlotte-Pipe-1-in-PVC-Sch-40-FPT-Cap-PVC021171200HD/203811724", use="Removable cover for HPC", leftover=0)
        def cap_1in():
            return cap(hpod, hpww)

        # Same here
        @bom_part("1in")
        @bom_part("1inx2ft PVC Sch. 40 Pipe", 1.98, link="http://www.homedepot.com/p/VPC-1-in-x-2-ft-PVC-Sch-40-Pipe-2201/202300506", use="HPC, High-Pressure Cylinder; SV10 body")
        def pipe_1inx2ft():
            return pipe(cylinderlength, hpod, hpww)

        def highpressurecylinder():

            return mirror([0,0,1])(
                up(bushingspacer/2 + exploded*3)(
                    pipe_1inx2ft()
                    +
                    up(cylinderlength + exploded*2)(
                        cap_1in()
                    )
                )
            )

        @bom_part("Lasco 2x1 MPTxFPT Reducer Bushing", 3.09, link="https://www.amazon.com/Lasco-439-249-Threaded-Reducer-Bushing%252c/dp/B004UHC0NY/ref=sr_1_1?ie=UTF8&qid=1469132094&sr=8-1&keywords=PVC+FPT+reducer+bushing", use="Connects LPC to HPC", leftover=0)
        def join():
            return reducer(2.64, lpod, lpww, hpod, hpww, bushingspacer)

        @bom_part("FIND PART")
        def plug():
            return tube(0.5, hpod - hpww*2, mainpiston_rod_d, center=True)

        return lowpressurecylinder() + highpressurecylinder() + join() + plug()

    """---Mainpiston---"""

    def mainpiston(self):
        r = mainpiston_rod_d/2

        @bom_part("FIND PART")
        def rod_1_25in():
            return cylinder(h = cylinderlength, r=r, center=True)

        @bom_part("FIND PART")
        def piston_2in():
            return piston(lpod - lpww*2, lpww, center=False)

        @bom_part("FIND PART")
        def piston_1in():
            return piston(hpod - hpww*2, hpww, center=False)

        return (
            rod_1_25in()
            +
            up(cylinderlength/2)(
                mirror([0,0,1])(
                    piston_2in()
                )
            )
            +
            down(cylinderlength/2)(
                piston_1in()
            )
        )

    """---Hole-Drilling---"""

    def fittings(self):
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

    def assembly(self):
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

        return (
            mainbody()  
            +
            rotate([0,90,0])(
                mainpiston()
            )
        )

if __name__ == "__main__":
    renderer.render(assembly())
