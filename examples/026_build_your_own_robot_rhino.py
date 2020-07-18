# Rhino
from compas.datastructures import Mesh
from compas.geometry import *
from compas.robots import Joint, RobotModel
from compas_fab.rhino import RobotArtist
from compas_fab.robots import Configuration

# create cylinder in yz plane
radius, length = 0.3, 5
cylinder = Cylinder(Circle(Plane([0, 0, 0], [1, 0, 0]), radius), length)
cylinder.transform(Translation([length / 2., 0, 0]))
mesh = Mesh.from_shape(cylinder)

# create robot
robot = RobotModel("robot", links=[], joints=[])
link0 = robot.add_link("world")

# Add all other links to robot
for count in range(1, 8):
    # add new link to robot
    robot.add_link("link" + str(count), visual_mesh=mesh.copy(), visual_color=(count * 0.72 % 1.0, count * 0.23 % 1.0 , 0.6))

    # add the joint between the last two links
    axis = (0, 0, 1)
    origin = Frame((length , 0, 0), (1, 0, 0), (0, 1, 0))
    robot.add_joint("joint" + str(count), Joint.CONTINUOUS, robot.links[-2] , robot.links[-1], origin, axis)

artist = RobotArtist(robot)
artist.clear_layer()

joint_names = robot.get_configurable_joint_names()
joint_values = [0.2] * len(joint_names)
joint_types = [Joint.CONTINUOUS] * len(joint_names)

config = Configuration(joint_values, joint_types)
artist.update(config, joint_names)
artist.draw_visual()
