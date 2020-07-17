import math

def show_trajectory(trajectory):
    import matplotlib.pyplot as plt
    # visualise
    positions = []
    velocities = []
    accelerations = []
    time_from_start = []

    for p in trajectory.points:
        positions.append(p.positions)
        velocities.append(p.velocities)
        accelerations.append(p.accelerations)
        time_from_start.append(p.time_from_start.seconds)
    
    plt.rcParams['figure.figsize'] = [17, 4]
    plt.subplot(131)
    plt.title('positions')
    plt.plot(positions)
    plt.subplot(132)
    plt.plot(velocities)
    plt.title('velocities')
    plt.subplot(133)
    plt.plot(accelerations)
    plt.title('accelerations')
    plt.show()


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
    frames = [picking_frame, savelevel_picking_frame]
    frames_tool0 = robot.from_attached_tool_to_tool0(frames)

    picking_frame_tool0 = robot.from_attached_tool_to_tool0([picking_frame])[0]
    picking_configuration = robot.inverse_kinematics(picking_frame_tool0, start_configuration)

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

    tolerance_position = 0.001
    tolerance_axes = [math.radians(1)] * 3

    target_frame = brick.gripping_frame.copy()
    target_frame.point += tolerance_vector

    savelevel_target_frame = target_frame.copy()
    savelevel_target_frame.point += savelevel_vector

    # Calculate goal constraints
    savelevel_target_frame_tool0 = robot.from_attached_tool_to_tool0([savelevel_target_frame])[0]
    goal_constraints = robot.constraints_from_frame(savelevel_target_frame_tool0,
                                                    tolerance_position,
                                                    tolerance_axes)

    moving_trajectory = robot.plan_motion(goal_constraints,
                                          start_configuration,
                                          planner_id='RRT',
                                          attached_collision_meshes=[attached_brick_mesh],
                                          num_planning_attempts=20,
                                          allowed_planning_time=10)

    
    frames = [savelevel_target_frame, target_frame]
    frames_tool0 = robot.from_attached_tool_to_tool0(frames)
    # as start configuration take last trajectory's end configuration
    last_configuration = moving_trajectory.points[-1]

    placing_trajectory = robot.plan_cartesian_motion(frames_tool0,
                                                     last_configuration,
                                                     max_step=0.01,
                                                     attached_collision_meshes=[attached_brick_mesh])
    return moving_trajectory, placing_trajectory