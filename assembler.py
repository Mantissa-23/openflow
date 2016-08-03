from __future__ import division, print_function;
import os
from solid import *
from solid.utils import *

import body
import spool
from utils import *
from plumbing import *

RESOLUTION = 0.1

set_bom_headers("link", "use", "leftover")

#Set to 1 to see exploded model w/ all parts. Set to a higher value for more separation.
exploded = 0

#Set to True to see hollow parts cut in half.
cutaway = True

"""---Assemblies---"""

def assemble(geometry):
    return (
        body.assembly()
        +
        spool.assembly()
    )

    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'Waterpump.py.scad')

    scad_render_to_file(assemble(), file_out, file_header='$fs = %s;' % RESOLUTION)

    bom = bill_of_materials(csv=True)

    print(bom)

