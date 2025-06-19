""" Basic model configs for Unitree Go2 """
import numpy as np
import os.path as osp

from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO

go2_action_scale = 0.5
go2_const_dof_range = dict(
    Hip_max= 1.0472,
    Hip_min= -1.0472,
    Front_Thigh_max= 3.4907,
    Front_Thigh_min= -1.5708,
    Rear_Thingh_max= 4.5379,
    Rear_Thingh_min= -0.5236,
    Calf_max= -0.83776,
    Calf_min= -2.7227,
)

class Go2RoughCfg( LeggedRobotCfg ):


    class init_state( LeggedRobotCfg.init_state ):
        pos = [0., 0., 0.5] # [m]
        default_joint_angles = { # 12 joints in the order of simulation
            "FL_hip_joint": 0.1,
            "FL_thigh_joint": 0.7,
            "FL_calf_joint": -1.5,
            "FR_hip_joint": -0.1,
            "FR_thigh_joint": 0.7,
            "FR_calf_joint": -1.5,
            "RL_hip_joint": 0.1,
            "RL_thigh_joint": 1.0,
            "RL_calf_joint": -1.5,
            "RR_hip_joint": -0.1,
            "RR_thigh_joint": 1.0,
            "RR_calf_joint": -1.5,
        }

    class init_state_slope( LeggedRobotCfg.init_state ):
        pos = [0.5, 0.0, 0.24] # x,y,z [m]
        default_joint_angles = { # = target angles [rad] when action = 0.0
            'FL_hip_joint': 0.03,   # [rad]
            'RL_hip_joint': 0.03,   # [rad]
            'FR_hip_joint': -0.03,  # [rad]
            'RR_hip_joint': -0.03,   # [rad]

            'FL_thigh_joint': 1.0,     # [rad]
            'RL_thigh_joint': 1.8,   # [rad]1.8
            'FR_thigh_joint': 1.0,     # [rad]
            'RR_thigh_joint': 1.8,   # [rad]

            'FL_calf_joint': -2.2,   # [rad]
            'RL_calf_joint': -1.2,    # [rad]
            'FR_calf_joint': -2.2,  # [rad]
            'RR_calf_joint': -1.2,    # [rad]
        }

    class control( LeggedRobotCfg.control ):
        # PD Drive parameters:
        control_type = 'P'
        stiffness = {'joint': 40.}  # [N*m/rad]
        damping = {'joint': 1.}     # [N*m*s/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = go2_action_scale
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 4
        computer_clip_torque = False
        motor_clip_torque = True

    class asset( LeggedRobotCfg.asset ):
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/go2/urdf/go2.urdf'
        name = "go2"
        foot_name = "foot"
        front_hip_names = ["FL_hip_joint", "FR_hip_joint"]
        rear_hip_names = ["RL_hip_joint", "RR_hip_joint"]
        penalize_contacts_on = ["thigh", "calf"]
        terminate_after_contacts_on = ["base"]#, "thigh", "calf"]
        self_collisions = 1 # 1 to disable, 0 to enable...bitwise filter
  
    class rewards( LeggedRobotCfg.rewards ):
        soft_dof_pos_limit = 0.9
        base_height_target = 0.25
        # class scales( LeggedRobotCfg.rewards.scales ):
            # torques = -0.0002
            # dof_pos_limits = -10.0

class Go2RoughCfgPPO( LeggedRobotCfgPPO ):
    class algorithm( LeggedRobotCfgPPO.algorithm ):
        entropy_coef = 0.01
    class runner( LeggedRobotCfgPPO.runner ):
        run_name = ''
        experiment_name = 'rough_go2'