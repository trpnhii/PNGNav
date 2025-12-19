#!/home/zhe/miniconda3/envs/pngenv/bin/python
from os.path import join

import rclpy
from rclpy.node import Node
import numpy as np

from png_navigation.configs.rrt_star_config import Config
from png_navigation.path_planning_classes.rrt_env_2d import Env
from png_navigation.path_planning_classes.irrt_star_2d import get_path_planner

from png_navigation.srv import SetEnv, SetEnvResponse
from png_navigation.srv import GetGlobalPlan, GetGlobalPlanResponse


def get_fake_env():
    env_dict = {
        'x_range': [0,10],
        'y_range': [0,10],
        'circle_obstacles': [],
        'rectangle_obstacles': [],
    }
    return Env(env_dict)

def get_fake_problem():
    problem = {
        'x_start': [0,0],
        'x_goal': [1,1],
        'search_radius': 10,
        'env': get_fake_env(),
    }
    return problem

class IRRTStarNode(Node):
    def __init__(
        self,
    ):
        super().__init__('png_navigation_irrt_star_node')
        self.config = Config()
        self.planner = get_path_planner(
            self.config.path_planner_args,
            get_fake_problem(),
            node=self,
        )
        self.set_env_service = self.create_service(SetEnv, 'png_navigation/set_env_2d', self.set_env)
        self.get_global_plan_service = self.create_service(GetGlobalPlan, 'png_navigation/get_global_plan', self.get_global_plan)
    
    def get_global_plan(self, request, response):
        self.planner.reset_robot(
            x_start=request.problem.start,
            x_goal=request.problem.goal,
            env=None,
            search_radius=request.problem.search_radius,
            max_time=request.problem.max_time,
        )
        # * clearance and max_iterations from plan_request are redundant and not used here.
        path = self.planner.planning_robot()
        if len(path) == 0:
            response.is_solved = False
            response.path = []
        else:
            response.is_solved = True
            response.path = path.flatten().tolist()
        return response

    def set_env(self, request, response):
        if len(request.env.circle_obstacles)>0:
            circle_obstacles = np.array(request.env.circle_obstacles).reshape(-1,3)
        else:
            circle_obstacles = []
        if len(request.env.rectangle_obstacles)>0:
            rectangle_obstacles = np.array(request.env.rectangle_obstacles).reshape(-1,4)
        else:
            rectangle_obstacles = []       
        env_dict = {
            'x_range': request.env.x_range,
            'y_range': request.env.y_range,
            'circle_obstacles': circle_obstacles,
            'rectangle_obstacles': rectangle_obstacles,
        }
        self.planner.reset_env_robot(Env(env_dict))
        self.get_logger().info("Environment is set.")
        response.is_set = True
        return response

def main():
    rclpy.init()
    irrtsn = IRRTStarNode()
    try:
        rclpy.spin(irrtsn)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()

