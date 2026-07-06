import yaml
import os
import subprocess
import time

# Sample lists for setups, votes, users, and instances
votes = ["A"]
vid_type =  "/normal_1080p" # "/downsample_480p"

# Create a dictionary of setups, each will have different setup and users
setups = {
    "phone_s22": ["Zeyu"],
    # "phone_s22": ["Wen"],
          }

# Base configuration dictionary
config = {
    "PACKAGE_ROOT": "./ptgaze",
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
        "dlib_model_path": "./ptgaze/dlib/shape_predictor_68_face_landmarks.dat",
        "mediapipe_max_num_faces": 1,
        "mediapipe_static_image_mode": False
    },
    "gaze_estimator": {
        "checkpoint": "./ptgaze/models/checkpoint_0015.pth",
        "camera_params": "./ptgaze/data/calib/sample_params.yaml",
        "use_dummy_camera_params": False,
        "normalized_camera_params": "./ptgaze/data/normalized_camera_params/mpiifacegaze.yaml",
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
            data_directory = "../data/" + setup + "/" + vote + vid_type
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
                config_filename = "config.yaml"
                with open(config_filename, 'w') as file:
                    yaml.dump(config, file)

                command = ["python", "ptgaze", "--config", config_filename]

                try:
                    result = subprocess.run(command, capture_output=True, text=True, check=True)
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