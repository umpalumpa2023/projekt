import cv2
import mediapipe as mp
import numpy as np

class Recognition:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def detect_person(self, frame):
        # Convert the BGR image to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        if not results.pose_landmarks:
            return None, None  # No person detected

        # Calculate center of mass from the landmarks
        landmarks = results.pose_landmarks.landmark
        valid_landmarks = [lm for lm in landmarks if lm.visibility > 0.5]  # Use only visible landmarks

        if len(valid_landmarks) == 0:
            return None, None

        # Calculate the average x and y coordinates for the center of mass
        com_x = int(np.mean([lm.x * frame.shape[1] for lm in valid_landmarks]))
        com_y = int(np.mean([lm.y * frame.shape[0] for lm in valid_landmarks]))

        return com_x, com_y
