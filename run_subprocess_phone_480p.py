import yaml
import os
import subprocess
import time

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'functions')))
from load_machine_config import load_machine_config

machine_config = load_machine_config()
proj_path = os.path.join(machine_config["data_dir"], "Phone_Privacy")

# Paths are built from this file's location, so the script works from any working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
ptgaze_dir = os.path.join(script_dir, "ptgaze")

# Sample lists for setups, votes, users, and instances
votes = ["A", "B", "C", "D", "E"]

# Create a dictionary of setups, each will have different setup and users
setups = {
    # "phone_s22": ["Jingwei", "Zeyu"],
    # "pad_op2": ["JingweiPad", "ZeyuPad"],

    # "phonesr_s22": ["Chuan", "Gujing", "Haofan", "Jimmy", "Jingwei", "Junwei", "Minjie", "minglei", "Mingxuan", "Rosie", "Sihang", "Wen", "Yirui", "Zeyu", "Zidan", "Ziyue", "Ziyue1"],
    # "phonedown_s22": ["Chuan", "Gujing", "Haofan", "Jimmy", "Jingwei", "Junwei", "Minjie", "minglei", "Mingxuan", "Rosie", "Sihang", "Wen", "Yirui", "Zeyu", "Zidan", "Ziyue", "Ziyue1"],
    
    # "phone180_s22": ["Chuan", "Jimmy", "minglei", "Zeyu", "Ziyue"],
    # "phone240_s22": ["Chuan", "Jimmy", "minglei", "Zeyu", "Ziyue"],
    # "phone180sr_s22": ["Chuan", "Jimmy", "minglei", "Zeyu", "Ziyue"],
    # "phone240sr_s22": ["Chuan", "Jimmy", "minglei", "Zeyu", "Ziyue"],

    "phone_s22": ["Haochen", "Linwei", "Rui", "Yipei", "Yu", "Ning", "Shengyan", "Wenl"],
    "pad_op2": ["HaochenPad", "LinweiPad", "NingPad", "RuiPad", "ShengyanPad", "WeiPad", "WenPad", "YipeiPad", "YuPad"],
    "phonerh_s22": ["Jingwei", "Ning", "Shengyan", "Wen"],
    "phoneds_s22": ["Jingwei", "Ning", "Shengyan", "Wen"],
    }

# Base configuration dictionary
config = {
    "PACKAGE_ROOT": ptgaze_dir,
    "mode": "MPIIFaceGaze",
    "device": "cuda",
    "model": {
        "name": "resnet_simple",
        "backbone": {
            "name": "resnet_simple",
            "pretrained": "resnet18",
            "resnet_block": "basic",
            "resnet_layers": [2, 2, 2]
        }
    },
    "face_detector": {
        "mode": "mediapipe",
        "dlib_model_path": os.path.join(ptgaze_dir, "dlib/shape_predictor_68_face_landmarks.dat"),
        "mediapipe_max_num_faces": 1,
        "mediapipe_static_image_mode": False
    },
    "gaze_estimator": {
        "checkpoint": os.path.join(ptgaze_dir, "models/checkpoint_0015.pth"),
        "camera_params": os.path.join(ptgaze_dir, "data/calib/sample_params.yaml"),
        "use_dummy_camera_params": False,
        "normalized_camera_params": os.path.join(ptgaze_dir, "data/normalized_camera_params/mpiifacegaze.yaml"),
        "normalized_camera_distance": 1.0,
        "image_size": [224, 224]
    },
    "demo": {
        "use_camera": False,
        "display_on_screen": False,
        "wait_time": 1,
        "data_directory": None,
        "image_path": None,
        "video_path": None,  # This will be updated in the loop
        "output_dir": None,
        "output_file_extension": "avi",
        "head_pose_axis_length": 0.05,
        "gaze_visualization_length": 0.05,
        "show_bbox": True,
        "show_head_pose": True,
        "show_landmarks": False,
        "show_normalized_image": False,
        "show_template_model": False
    }
}

# Loop through the variables and construct the video path for each combination
for setup in setups:
    users = setups[setup]
    print("Running setup: ", setup)
    print("Users: ", users)
    for vote in votes:
        for user in users:
            data_directory = proj_path + "/data/" + setup + "/" + vote + "/downsample_480p"
            config['demo']['data_directory'] = data_directory
            # find all video files in the data path end with ".mp4"
            all_files = os.listdir(data_directory)
            video_files = [f for f in all_files if f.endswith(".mp4") and f.startswith(user)]
            for ins, video in enumerate(video_files):
                time_start = time.time()
                # Construct the video path dynamically based on the current loop variables
                video_path = os.path.join(data_directory, video)

                config['demo']['video_path'] = video_path
                config['demo']['output_dir'] = data_directory + "/angle"
                config_filename = os.path.join(script_dir, "config.yaml")
                with open(config_filename, 'w') as file:
                    yaml.dump(config, file)

                command = ["python", "-m", "ptgaze", "--config", config_filename]

                try:
                    result = subprocess.run(command, capture_output=True, text=True, check=True, cwd=script_dir)
                    output = result.stdout
                    error_output = result.stderr
                    print("Run with \"" + video_path + "\" executed successfully!")
                    time_end = time.time()
                    print("Time used: ", round(time_end - time_start, 3), " seconds")
                    # print("Output:\n", output)
                    # # Check if there was any error output
                    # if error_output:
                    #     print("Error Output:\n", error_output)

                except subprocess.CalledProcessError as e:
                    print(f"Error occurred with {setup}, {vote}, {user}, {ins}!")
                    print("Error message:\n", e.stderr)