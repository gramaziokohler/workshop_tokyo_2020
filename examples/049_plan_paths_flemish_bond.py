import os
import math
import time
import json
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Transformation
from compas_fab.backends import RosClient
from compas_fab.robots import PlanningScene
from compas_fab.robots import Configuration
from compas_fab.robots import Tool
from compas_fab.robots import AttachedCollisionMesh
from compas_fab.robots import CollisionMesh
from assembly import Element, Assembly

# Path settings
HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
PATH_TO = os.path.join(DATA, os.path.splitext(os.path.basename(__file__))[0] + ".json")

# Load assembly settings and create instances
settings_file = os.path.join(DATA, "settings.json")
with open(settings_file, 'r') as f:
    data = json.load(f)

width, length, height = data['brick_dimensions']
tolerance_vector = Vector.from_data(data['tolerance_vector'])
savelevel_vector = Vector.from_data(data['savelevel_vector'])
brick = Element.from_data(data['brick'])
start_configuration = Configuration.from_data(data['start_configuration'])
picking_frame = Frame.from_data(data['picking_frame'])
savelevel_picking_frame = picking_frame.copy()
savelevel_picking_frame.point += savelevel_vector
picking_frame.point += tolerance_vector

# create tool from json
filepath = os.path.join(DATA, "vacuum_gripper.json")
tool = Tool.from_json(filepath)

# load assembly from file
filepath = os.path.join(DATA, '048_flemish_bond.json')
# load from existing if calculation failed at one point...

clear_planning_scene = True

if os.path.isfile(PATH_TO):
    assembly = Assembly.from_json(PATH_TO)
    clear_planning_scene = False
else:
    assembly = Assembly.from_json(filepath)

# create an attached collision mesh to be attached to the robot's end effector.
T = Transformation.from_frame_to_frame(brick.gripping_frame, tool.frame)
brick_tool0 = brick.transformed(T)
attached_brick_mesh = AttachedCollisionMesh(CollisionMesh(brick_tool0.mesh, 'brick'), 'ee_link')

# ==============================================================================
# From here on: fill in code, whereever you see this dots ...


def plan_picking_motion(robot, picking_frame, savelevel_picking_frame, start_configuration, attached_brick_mesh):
    """Returns a cartesian trajectory to pick an element.

    Parameters
    ----------
    robot : :class:`compas.robots.Robot`
    picking_frame : :class:`Frame`
    save_level_picking_frame : :class:`Frame`
    start_configuration : :class:`Configuration`
    attached_brick_mesh : :class:`AttachedCollisionMesh`

    Returns
    -------
    :class:`JointTrajectory`
    """

    # Calculate frames at tool0 and picking_configuration
    # ...
    picking_trajectory = robot.plan_cartesian_motion(frames_tool0,
                                                     picking_configuration,
                                                     max_step=0.01,
                                                     attached_collision_meshes=[attached_brick_mesh])
    return picking_trajectory


def plan_moving_and_placing_motion(robot, brick, start_configuration, tolerance_vector, savelevel_vector, attached_brick_mesh):
    """Returns two trajectories for moving and placing a brick.

    Parameters
    ----------
    robot : :class:`compas.robots.Robot`
    brick : :class:`Element`
    start_configuration : :class:`Configuration`
    tolerance_vector : :class:`Vector`
    savelevel_vector : :class:`Vector`
    attached_brick_mesh : :class:`AttachedCollisionMesh`

    Returns
    -------
    list of :class:`JointTrajectory`
    """

    # Calculate goal constraints
    # ...

    moving_trajectory = robot.plan_motion(goal_constraints,
                                          start_configuration,
                                          planner_id='RRT',
                                          attached_collision_meshes=[attached_brick_mesh],
                                          num_planning_attempts=20,
                                          allowed_planning_time=10)

    # as start configuration take last trajectory's end configuration
    # last_configuration = ...
    
    # ...

    placing_trajectory = robot.plan_cartesian_motion(frames_tool0,
                                                     last_configuration,
                                                     max_step=0.01,
                                                     attached_collision_meshes=[attached_brick_mesh])
    return moving_trajectory, placing_trajectory

# NOTE: If you run Docker Toolbox, change `localhost` to `192.168.99.100`
with RosClient('localhost') as client:

    robot = client.load_robot()
    scene = PlanningScene(robot)
    robot.attach_tool(tool)

    # 1. Add a collison mesh to the planning scene: floor, desk, etc.
    # ...

    if clear_planning_scene:
        scene.remove_collision_mesh('brick_wall')
        time.sleep(0.1)

    # 2. Compute picking trajectory
    # picking_trajectory = ...

    # 3. Save the last configuration from that trajectory as new start_configuration
    # start_configuration = ...

    sequence = [key for key in assembly.network.vertices()]
    exclude_keys = [
        vkey for vkey in assembly.network.vertices_where({'is_planned': True})]
    sequence = [k for k in sequence if k not in exclude_keys]

    for key in sequence:
        print("=" * 30 + "\nCalculating path for brick with key %d." % key)

        brick = assembly.element(key)

        # 4. Create an attached collision mesh and attach it to the robot's end effector.
        T = Transformation.from_frame_to_frame(brick.gripping_frame, tool.frame)
        brick_tool0 = brick.transformed(T)
        ee_link_name = robot.get_end_effector_link_name()
        attached_brick_mesh = AttachedCollisionMesh(CollisionMesh(brick_tool0.mesh, 'brick'), ee_link_name)

        # 5. Calculate moving_ and placing trajectories
        # moving_trajectory, placing_trajectory = ...

        # 6. Add the brick to the planning scene and wait a bit after that
        # ...

        # 7. Add calculated trajectories to element and set to 'planned'
        brick.trajectory = picking_trajectory.points + moving_trajectory.points + placing_trajectory.points
        assembly.network.set_vertex_attribute(key, 'is_planned', True)

        # 8. Save assembly to json after every placed element
        assembly.to_json(PATH_TO, pretty=True)