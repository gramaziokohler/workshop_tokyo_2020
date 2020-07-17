"""Example: Bring a box from the world coordinate system into another coordinate
system and view in Rhino.
"""
from compas.geometry import Frame
from compas.geometry import Box
from compas.datastructures import Mesh
from compas_rhino.artists import FrameArtist
from compas_rhino.artists import MeshArtist

# Box in the world coordinate system
frame = Frame([1, 0, 0], [-0.45, 0.1, 0.3], [1, 0, 0])
width, length, height = 1, 1, 1
box = Box(frame, width, length, height)

# Frame F representing a coordinate system
F = Frame([2, 2, 2], [0.978, 0.010, -0.210], [0.090, 0.882, 0.463])

# Represent box frame in frame F and construct new box
box_frame_transformed = F.to_world_coords(box.frame)
box_transformed = Box(box_frame_transformed, width, length, height)
print("Box frame transformed:", box_transformed.frame)

# create artists
artist1 = FrameArtist(Frame.worldXY())
artist2 = MeshArtist(Mesh.from_shape(box))
artist3 = FrameArtist(F)
artist4 = MeshArtist(Mesh.from_shape(box_transformed))

# draw
artist1.draw()
artist2.draw_faces()
artist3.draw()
artist4.draw_faces()
