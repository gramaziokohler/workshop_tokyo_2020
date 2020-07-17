import os
import json

import compas
from compas.geometry import Translation
from assembly import Element
from assembly import Assembly

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
PATH_TO = os.path.join(DATA, os.path.splitext(os.path.basename(__file__))[0] + ".json")


# load settings (shared by GH)
settings_file = os.path.join(DATA, "settings.json")
with open(settings_file, 'r') as f:
    data = json.load(f)

# Get from settings
brick = Element.from_data(data['brick'])
halfbrick = Element.from_data(data['halfbrick'])
width, length, height = data['brick_dimensions']

COURSES = 3
BRICKS_PER_COURSE = 5

MORTAR_PERPENDS = 0.003
MORTAR_BEDS = 0.003

assembly = Assembly()

total_length = BRICKS_PER_COURSE * width + (BRICKS_PER_COURSE - 1) * MORTAR_PERPENDS
gap_even = MORTAR_PERPENDS
gap_uneven = (total_length - (BRICKS_PER_COURSE * width))/BRICKS_PER_COURSE


for row in range(COURSES):
    dy = row * height
    half_brick_ends = row % 2 != 0
    gap = gap_even if row % 2 == 0 else gap_uneven
    dx = 0

    bricks_in_course = BRICKS_PER_COURSE + (1 if half_brick_ends else 0)
    for j in range(bricks_in_course):

        first = j == 0
        last = j == bricks_in_course - 1

        is_half_brick = (first or last) and half_brick_ends

        if is_half_brick:
            T = Translation([dx - width/2, 0, dy])
            assembly.add_element(halfbrick.transformed(T))
            dx += width/2
        else:
            T = Translation([dx, 0, dy])
            assembly.add_element(brick.transformed(T))
            dx += width

        dx += gap


assembly.transform(Translation([-0.26, -0.28, 0]))

# 6. Save assembly to json
assembly.to_json(PATH_TO)

# Run this in rhino
if compas.IPY:
    from assembly.rhino import AssemblyArtist
    artist = AssemblyArtist(assembly, layer='COMPAS::Assembly')
    artist.clear_layer()
    artist.draw()
