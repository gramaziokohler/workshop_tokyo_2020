import os
import time

from compas_fab.backends import RosClient
from compas_fab.robots import PlanningScene
from compas_fab.robots import Tool

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
tool = Tool.from_json(os.path.join(DATA, "vacuum_gripper.json"))

with RosClient('localhost') as client:
    robot = client.load_robot()
    scene = PlanningScene(robot)

    # Attach the tool
    robot.attach_tool(tool)
    scene.add_attached_tool()

    time.sleep(3)

    # Remove the tool
    scene.remove_attached_tool()
    scene.remove_collision_mesh(tool.name)
    robot.detach_tool()
    time.sleep(1)
