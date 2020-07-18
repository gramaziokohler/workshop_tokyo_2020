import time

from compas.datastructures import Mesh

import compas_fab
from compas_fab.backends import RosClient
from compas_fab.robots import CollisionMesh
from compas_fab.robots import PlanningScene

with RosClient('localhost') as client:
    robot = client.load_robot()

    scene = PlanningScene(robot)

    # create collison objects
    mesh = Mesh.from_stl(compas_fab.get('planning_scene/cone.stl'))
    cm = CollisionMesh(mesh, 'tip')

    # attach it to the end-effector
    group = robot.main_group_name
    scene.attach_collision_mesh_to_robot_end_effector(cm, group=group)

    # sleep a bit before removing collision mesh
    time.sleep(3)

    scene.remove_attached_collision_mesh('tip')
    scene.remove_collision_mesh('tip')
    time.sleep(1)
