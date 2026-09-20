#!/usr/bin/env python3
"""Starter node for the Lunabotics ROS 2 case study.

Fill in TASKS 1-3 here. See README.md for the full description of each task.

Run it with:

    ros2 run move publisher

As shipped this node starts, spins, and does nothing -- that is intentional. Use it to
confirm your workspace is built and sourced before you write any logic.

Each task is marked with a TASK n.n comment matching the README. Commented-out lines are
deliberate: uncomment and complete them.
"""

import bisect
import math

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Float64


class RobotController(Node):
    """Drives the robot, tracks its position error, and flags obstacles."""

    def __init__(self):
        super().__init__("robot_controller")

        self.start_time = self.get_clock().now()

        # Publish to /error when the position delta exceeds this (TASK 2.3).
        # This is a starting value -- justify whatever you settle on.
        self.error_thresh = 0.5

        # ---- TASK 1.2: publisher that drives the robot ---------------------
        # Which topic moves the robot? Find it first (TASK 1.1), then uncomment.
        #
        self.move_pub = self.create_publisher(Twist, "cmd_vel", 10)
        #
        # Then drive it on a timer:
        self.move_timer = self.create_timer(0.01, self.send_move_cmd)

        # ---- TASK 1.3: the path you chose ----------------------------------
        # Pick a route that gets the robot around the wall, and represent it
        # however you think is best -- a list of waypoints, a sequence of
        # timed velocity commands, a parametric curve, something else.
        #
        # Document HERE why you chose this path and this representation.
        # That reasoning is a large part of what we are evaluating.

        """
        These three points represent a bezier curve, basically exploiting the fact
        that bezier curves have matrix representations, meaning that for a quadratic
        bezier their parametric equations can be derived from just these three points
        (though we don't need to actually derive the equations or the matrix). This 
        means that I can define the entire path with 3 points (more if needed), making
        it really easy to adjust on the fly than a list of points or a sequence of 
        timed velocity commands.

        From there, I get the current position from the odometry, find the closest
        point on the bezier curve (since realistically we're not on it), compute the t
        value of that point, look ahead a small amount, and use some pure pursuit
        algorithms to get the target translational and angular velocities. I've commented
        throughout all the methods I've used for this math, so for more details, look there.

        This specific bezier was chosen through manual testing via the gazebo simulation:
        The start point and end points are pretty much fixed, so I was just messing with
        the control point to adjust the curvature of the path. Since I only needed to
        mess with one point thanks to this representation, this was pretty quick.

        Full disclaimer: a lot of this code is a simpler version of stuff I used in
        a path following library I wrote in high school for FTC, with the main difference
        being using pure pursuit algorithms to adjust for differential drive as previously 
        I'd only worked with holonomic drivetrains like mecanum and swerve.
        """
        self.path = (
            (0.0, 0.0),  # start
            (6.0, -8),  # control point
            (8.0, -2.7),  # end
        )

        # precomputes a table of 500 points and their positions
        # on the curve in terms of arc length
        self.arc_ts, self.arc_distances = build_arc_length_table(self.path)

        # meters
        self.lookahead_dist = 0.8

        self.last_t = 0.0

        self.end_x, self.end_y = self.path[-1]

        self.robot_x = None
        self.robot_y = None
        self.robot_heading = None
        self.odom_sub = self.create_subscription(
            Odometry,
            "/model/vehicle_blue/odometry",
            self.update_pose,
            qos_profile_sensor_data,
        )

        # ---- TASK 2.2: subscriber for the robot's 6D pose ------------------
        # One of the two onboard sensors reports 6D data. Find it (TASK 2.1).
        #
        # self.robot_pos_sub = self.create_subscription(
        #     <TODO: msg type>,
        #     '<TODO: topic name>',
        #     self.on_robot_pos,
        #     qos_profile_sensor_data,
        # )

        # ---- TASK 2.3: where the measured-vs-actual error goes -------------
        # self.error_pub = self.create_publisher(Float64, '/error', 10)
        #
        # Hint: ground truth for "actual" is published by the simulator on the
        # robot's odometry topic (nav_msgs/Odometry). Deciding what to compare,
        # and in which frame, is part of the task.

        # ---- TASK 3: lidar in, filtered obstacles out ----------------------
        # The lidar has a single vertical sample, so this cloud is one flat
        # row of points at the sensor's height -- not a 3D volume.
        #
        # self.lidar_sub = self.create_subscription(
        #     PointCloud2,
        #     '/lidar/points',
        #     self.on_lidar,
        #     qos_profile_sensor_data,
        # )
        # self.obstacle_pub = self.create_publisher(
        #     PointCloud2, '/obstacle_cloud', 10)

        self.get_logger().info(
            "robot_controller started (scaffold -- nothing wired up yet)"
        )

    def update_pose(self, msg):
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y

        # learning about quaternions was fun!
        q = msg.pose.pose.orientation

        self.robot_heading = math.atan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z),
        )

        # self.get_logger().info(
        #     f"x={self.robot_x:.3f}, y={self.robot_y:.3f}, "
        #     f"heading={self.robot_heading:.3f}"
        # )

    # -----------------------------------------------------------------------
    # TASK 1.2 -- publish a velocity command
    # -----------------------------------------------------------------------
    def send_move_cmd(self):
        """Publish one Twist that moves the robot along self.path.

        TODO: build the Twist and publish it on self.move_pub.
        """
        twist = Twist()

        if self.robot_x is None or self.robot_y is None or self.robot_heading is None:
            return

        t = closest_t(
            self.robot_x,
            self.robot_y,
            self.path,
            self.last_t,
        )

        self.get_logger().info(
            f"current_t= {self.last_t:3f}, closest_t= {t:3f}, diff={abs(t - self.last_t):3f}"
        )

        # make sure it goes forward, not back
        t = max(t, self.last_t)
        self.last_t = t

        end_dist = math.hypot(
            self.end_x - self.robot_x,
            self.end_y - self.robot_y,
        )

        # stop when done
        if t >= 0.995 or end_dist < 0.1:
            # i think this is the default but just to be explicit
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.move_pub.publish(twist)
            return

        # look slightly forward on path
        # target_t = min(t + 0.05, 1.0)
        target_t = get_lookahead_t_binary(
            t,
            self.lookahead_dist,
            self.arc_ts,
            self.arc_distances,
        )
        target_x, target_y = get_point_at_t_value(target_t, self.path)

        # coords relative to robot
        dx = target_x - self.robot_x
        dy = target_y - self.robot_y

        c = math.cos(self.robot_heading)
        s = math.sin(self.robot_heading)

        local_x = c * dx + s * dy
        local_y = -s * dx + c * dy

        # pure pursuit algos i found
        lookahead_sq = local_x**2 + local_y**2

        if lookahead_sq > 1e-6:
            curvature = 2.0 * local_y / lookahead_sq
        else:
            curvature = 0.0

        max_velocity = 3.0
        max_angular_vel = 1.0

        velocity = min(max_velocity, end_dist * 0.8)

        if abs(curvature) > 1e-6:
            # slow down on turns -- helps at high speeds
            velocity = min(
                velocity,
                max_angular_vel / abs(curvature),
            )

        target_angular_vel = velocity * curvature

        twist.linear.x = float(velocity)
        twist.angular.z = float(target_angular_vel)

        self.move_pub.publish(twist)

    # -----------------------------------------------------------------------
    # TASK 2.3 -- compare reported position against ground truth
    # -----------------------------------------------------------------------
    def on_robot_pos(self, msg):
        """Compare the sensor's idea of where we are against the truth.

        Publish a Float64 on self.error_pub when the delta exceeds
        self.error_thresh.

        TODO: decide what "delta" means here and justify it in a comment.
        """
        raise NotImplementedError("TASK 2.3")

    # -----------------------------------------------------------------------
    # TASK 3.3 -- classify a single lidar point
    # -----------------------------------------------------------------------
    def is_obstacle(self, point):
        """Return True if `point` is something we must avoid.

        The barrier is passable -- treat it like dust in the air. The poles are
        not. `point` is an (x, y, z) tuple in the lidar's frame.

        TODO: decide what separates a pole from the barrier and implement it.
        """
        raise NotImplementedError("TASK 3.3")

    # -----------------------------------------------------------------------
    # TASK 3.2 -- filter the scan and republish what matters
    # -----------------------------------------------------------------------
    def on_lidar(self, msg):
        """Filter incoming points through is_obstacle and republish.

        point_cloud2.read_points(msg, field_names=('x', 'y', 'z')) iterates the
        cloud; point_cloud2.create_cloud_xyz32(msg.header, pts) builds the
        outgoing one.

        TODO: keep only the obstacle points and publish on self.obstacle_pub.
        """
        raise NotImplementedError("TASK 3.2")


def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


# find point on path given a t value where t = 0 is the starting point
# and t = 1 is the end point.
# Note: as written only works for quadratic beziers,
# generalization not necessary for this task
def get_point_at_t_value(
    t: float, path: tuple[tuple[float, float], ...]
) -> tuple[float, float]:

    p0, p1, p2 = path

    a = lerp(p0, p1, t)
    b = lerp(p1, p2, t)

    return lerp(a, b, t)


# needs previous closest t-value
# computes a much closer approximation of
# t-value given the previous t_value.
# assumes robot hasn't moved much between loops
def closest_t(x: float, y: float, path: tuple[tuple[float, float], ...], prev_t: float):
    def dist_sq(t):
        px, py = get_point_at_t_value(t, path)
        return (px - x) ** 2 + (py - y) ** 2

    lo = max(0.0, prev_t - 0.1)
    hi = min(1.0, prev_t + 0.1)

    # ternary search
    for _ in range(15):
        t1 = lo + (hi - lo) / 3
        t2 = hi - (hi - lo) / 3

        if dist_sq(t1) < dist_sq(t2):
            hi = t2
        else:
            lo = t1

    return (lo + hi) / 2


# checks num_loops equally spaced (by t-value) points
# on the curve to approximate the
# t value of the closest point on the curve
# (since more than likely you're not exactly
# on the curve)

"""
def brute_force_closest_t(
    x: float, y: float, path: tuple[tuple[float, float], ...], num_loops: int
):
    best_t = 0.0
    best_dist = float("inf")

    # fine tune loop nums as needed
    for i in range(num_loops):
        t = i / float(num_loops - 1)
        px, py = get_point_at_t_value(t, path)

        # dist is squared here, but no point
        # computing sqrt for js comparing
        dist = (px - x) ** 2 + (py - y) ** 2

        if dist < best_dist:
            best_dist = dist
            best_t = t

    return best_t
"""


# compute a t value to look ahead to by
# traveling a certain amount on the curve. This
# is far move effective than computing via t-value
# because it isn't affected by the length of the curve
def get_lookahead_t(
    start_t: float,
    path: tuple[tuple[float, float], ...],
    lookahead_dist: float,
    step: float = 0.005,
) -> float:
    t = start_t
    prev_x, prev_y = get_point_at_t_value(t, path)
    distance_traveled = 0.0

    while t < 1.0 and distance_traveled < lookahead_dist:
        next_t = min(t + step, 1.0)
        x, y = get_point_at_t_value(next_t, path)

        distance_traveled += math.hypot(
            x - prev_x,
            y - prev_y,
        )

        prev_x, prev_y = x, y
        t = next_t

    return t


# computes two lists of length 500, where one
# is t-values and the other is the total arc length
# from the start of the curve to the point with that
# t-value in meters. Then, we can subtract as needed
# to get the difference between any two points
def build_arc_length_table(
    path: tuple[tuple[float, float], ...],
    num_samples: int = 500,
) -> tuple[list[float], list[float]]:
    ts = [0.0]
    distances = [0.0]

    prev_x, prev_y = get_point_at_t_value(0.0, path)
    total_dist = 0.0

    for i in range(1, num_samples + 1):
        t = i / float(num_samples)
        x, y = get_point_at_t_value(t, path)

        # linear approximation is close enough with 500 points
        total_dist += math.hypot(x - prev_x, y - prev_y)

        ts.append(t)
        distances.append(total_dist)

        prev_x, prev_y = x, y

    return ts, distances


# gets the arc length from the start
# of the curve to the point at a given t-value
# by adding up the total length up to the previous
# point and adding the linear approximation of the
# distance between this point and the previous one
def arc_length_at_t(
    t: float,
    ts: list[float],
    distances: list[float],
) -> float:
    i = bisect.bisect_left(ts, t)

    if i == 0:
        return distances[0]
    if i >= len(ts):
        return distances[-1]

    alpha = (t - ts[i - 1]) / (ts[i] - ts[i - 1])

    return distances[i - 1] + alpha * (distances[i] - distances[i - 1])


# given closest t-value on the path,
# computes the point with that is a certain
# distance along the path ahead for lookahead
# purposes
def get_lookahead_t_binary(
    current_t: float,
    lookahead_dist: float,
    ts: list[float],
    distances: list[float],
) -> float:
    current_dist = arc_length_at_t(current_t, ts, distances)
    target_dist = current_dist + lookahead_dist

    i = bisect.bisect_left(distances, target_dist)

    if i >= len(ts):
        return 1.0
    if i == 0:
        return ts[0]

    d0 = distances[i - 1]
    d1 = distances[i]

    if d1 == d0:
        return ts[i]

    alpha = (target_dist - d0) / (d1 - d0)

    return ts[i - 1] + alpha * (ts[i] - ts[i - 1])


# simple linear interpolation between two points
# at a given t-value from [0, 1]
def lerp(
    p0: tuple[float, float],
    p1: tuple[float, float],
    t: float,
) -> tuple[float, float]:
    return (
        p0[0] + t * (p1[0] - p0[0]),
        p0[1] + t * (p1[1] - p0[1]),
    )


if __name__ == "__main__":
    main()
