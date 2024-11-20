import cv2
import numpy as np
from openpose import pyopenpose as op  # Make sure OpenPose Python API is available

class Recognition:
    def __init__(self, model_folder='path/to/openpose/models'):
        params = {
            "model_folder": model_folder,
            "net_resolution": "-1x368"  # Adjust this based on performance requirements
        }
        self.op_wrapper = op.WrapperPython()
        self.op_wrapper.configure(params)
        self.op_wrapper.start()

    def detect_person_center(self, frame):
        datum = op.Datum()
        datum.cvInputData = frame
        self.op_wrapper.emplaceAndPop([datum])

        # Extract keypoints if detected
        keypoints = datum.poseKeypoints
        if keypoints is None or len(keypoints.shape) != 3:
            return None, None  # No person detected

        # Calculate center of mass (average of detected keypoints)
        person_keypoints = keypoints[0]  # Assuming single person detection for simplicity
        valid_keypoints = person_keypoints[person_keypoints[:, 2] > 0]  # Use only detected points with confidence > 0

        if len(valid_keypoints) == 0:
            return None, None

        # Calculate the average x and y coordinates as the center of mass
        com_x = int(np.mean(valid_keypoints[:, 0]))
        com_y = int(np.mean(valid_keypoints[:, 1]))
        return com_x, com_y
