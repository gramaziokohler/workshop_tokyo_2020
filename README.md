# COMPAS FAB: Hands-on intro, Tokyo 18.07.2020

During this session we will install and play around with `COMPAS` core framework and its robotic fabrication extension: `COMPAS FAB`. The goal is to end up with the tools ready to do kinematics and planning on any supported robot.

## Overview

* Intro & Session goals
* COMPAS 101
* COMPAS FAB
* Robotics: fundamentals, models & backends
* ROS primer
* Kinematics & Motion planning
* What's next?

## Resources

* **Presentation**: [Slides](https://docs.google.com/presentation/d/1MwbF9ibyxKD2Nxk989vYtSyW_or0pXSVWBnFI-EQtdM/edit?usp=sharing)
* **Documentation**:
  * [COMPAS API Reference](https://compas-dev.github.io/main/api.html)
  * [COMPAS FAB API Reference](https://gramaziokohler.github.io/compas_fab/latest/reference.html)

## Examples

### Robotic fundamentals

* `Frame` examples:
  * [Several ways to construct a `Frame`](examples/001_several_ways_to_construct_frame.py)
  * [`Point` in `Frame`](examples/002_point_in_frame.py)
  * [`Frame` in `Frame`](examples/003_frame_in_frame.py)
  * [Bring a box from the world coordinate frame into another coordinate frame](examples/004_box_from_the_world_to_local.py)
  * [Use artists to draw the box in Rhino](examples/005_box_from_the_world_to_local_rhino.py)
* `Transformation` examples:
  * [Several ways to construct a `Transformation`](examples/006_examples_transformation.py)
  * [Inverse transformation](examples/007_inverse_transformation.py)
  * [Pre-multiply transformations](examples/008_premultiply_transformations.py)
  * [Pre- vs. post-multiplication](examples/009_pre_vs_post_multiplication.py)
  * [Decompose transformation](examples/010_decompose_transformation.py)
  * [Transform `Point` and `Vector`](examples/011_transform_point_and_vector.py)
  * [Transformation of multiple points](examples/012_transform_multiple.py)
  * [Change-basis transformation vs. transformation between frames](examples/013_change_basis_vs_between_frames.py)
  * [Bring a box from the world coordinate frame into another coordinate frame](examples/014_box_from_the_world_to_local.py)
  * [Use artists to draw the box in Rhino](examples/015_box_from_the_world_to_local_rhino.py)
* `Rotation` examples:
  * [Several ways to construct a `Rotation`](examples/016_several_ways_to_construct_rotation.py)
  * [Different Robot vendors use different conventions to describe TCP orientation](examples/017_robot_tcp_orientations.py)
  * [Euler angles example](examples/018_euler_angles.py)
  * [Axis-angle example](examples/019_axis_angle.py)
  * [Unit Quaternion example](examples/020_quaternion.py)

### Robot model and ROS

* [Docker configuration to launch ROS & MoveIt](docker/)
* Open MoveIt! in your browser:
  * `http://localhost:8080/vnc.html?resize=scale&autoconnect=true`
* Basic examples:
  * [Programatically define a robot](examples/021_define_model.py)
  * [Load robots from Github](examples/022_robot_from_github.py)
  * [Load robots from ROS](examples/023_robot_from_ros.py)
  * [Visualize robots in Rhino](examples/024_robot_artist_rhino.py)
  * [Visualize robots in Grasshopper](examples/025_robot_artist_grasshopper.ghx)
  * [Build your own robot](examples/026_build_your_own_robot_rhino.py)
* Basic ROS examples:
  * [Verify connection](examples/027_check_connection.py)
  * The cannonical example of ROS: chatter nodes
    * [Talker node](examples/028_ros_hello_world_talker.py)
    * [Listener node](examples/029_ros_hello_world_listener.py)
* Examples of ROS & MoveIt planning with UR5:
  * [Forward Kinematics](examples/030_forward_kinematics_ros_loader.py)
  * [Inverse Kinematics](examples/031_inverse_kinematics_ros_loader.py)
  * [Cartesian motion planning](examples/032_plan_cartesian_motion_ros_loader.py)
  * [Free space motion planning](examples/033_plan_motion_ros_loader.py)
  * Planning scene management:
    * [Add objects to the scene](examples/034_add_collision_mesh.py)
    * [Append nested objects to the scene](examples/035_append_collision_meshes.py)
    * [Remove objects from the scene](examples/036_remove_collision_mesh.py)
* [Grasshopper Playground](examples/038_robot_playground_ur5.ghx)
* Attaching gripper/tool:
  * [Attach tool to last link of the robot](examples/041_attach_tool.py)
  * [Plan cartesian motion with attached tool](examples/042_plan_cartesian_motion_with_attached_tool.py)

## Requirements

Please make sure you have the following software installed on your laptop *before* the session:

1. Minimum OS: Windows 10 Pro or Mac OS Sierra 10.12
2. Anaconda 3: https://www.anaconda.com/distribution/
3. Docker Desktop: https://www.docker.com/products/docker-desktop

    **NOTE**: After installation on Windows, it is required to enable `Virtualization` on the BIOS of the computer. If you don't know how to do this, please ask on the Discord channel!

4. Rhino 6 & Grasshopper: https://www.rhino3d.com/download
5. Visual Studio Code: https://code.visualstudio.com/

    Any python editor works, but we recommend VS Code + extensions, see doc: https://gramaziokohler.github.io/compas_fab/latest/getting_started.html#working-in-visual-studio-code-1

6. Once installation is done, pull one of our docker images. To do that, open the Anaconda prompt or Terminal and execute the following:

        docker pull gramaziokohler/ros-ur-planner

## Installation

We use `conda` to make sure we have clean, isolated environment for dependencies.

First time using `conda`? Make sure you run this at least once:

    (base) conda config --add channels conda-forge

Create a new conda environment:

**Windows**

    (base) conda create -n tokyo20 python=3.8 compas_fab=0.11 --yes
    (base) conda activate tokyo20

**Mac**

    (base) conda create -n tokyo20 python=3.8 compas_fab=0.11 python.app --yes
    (base) conda activate tokyo20

### Verify installation

    (tokyo20) pip show compas_fab
    Name: compas-fab
    Version: 0.11.0
    Summary: Robotic fabrication package for the COMPAS Framework
    ...

### Install on Rhino

    (tokyo20) python -m compas_fab.rhino.install

NOTE: This installs to Rhino 6.0, use `-v 5.0` if needed.
