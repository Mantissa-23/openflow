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

# Refactor the spool so it's more accurate to what we're actually going to do.
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

    @bom_part("1-1/4 in. PVC Sch. 40 FPT Cap", 0.50, link="https://www.amazon.com/Lasco-448-012-Threaded-Cap%252c-LASCO/dp/B0195UH0U8/ref=sr_1_1?ie=UTF8&qid=1469131420&sr=8-1&keywords=1-1%2F4+in.+PVC+cap+FPT", use="Removable covers for SV10", leftover=0)
    def valve_cap():
        return cap(od, oww)

    @bom_part("1-1/4in. x 2ft. PVC Sch. 40 Pipe", 3.20, link="http://www.homedepot.com/p/Charlotte-Pipe-1-1-4-in-x-2-ft-PVC-Sch-40-Pipe-PVC-07100-0200/202018045", use="SV10 Body", leftover='12"')
    def pipe_body():
        return pipe(length + endpadding*2, od, oww, center=True)

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
            pipe_body()
            +
            up(tn*length/2)(
                mirror([0,0,t])(
                    valve_cap()
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

def five_valve_assembly(top=True):
    return five_valve(6, spoolouterod, spoolouterww, spoolinnerod, spoolinnerww, top=top, center=False)

def assembly():
    return forward(6)(
        rotate([0,90,0])(
            five_valve_assembly()
            +
            down(6 + spoolouterww*2)(
                five_valve_assembly(top=False)
            )
        )
    )

