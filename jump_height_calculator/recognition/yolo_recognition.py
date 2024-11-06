# recognition/yolo_recognition.py

import cv2
from ultralytics import YOLO
from .recognition_base import RecognitionSoftware

class YOLORecognition(RecognitionSoftware):
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)

    def detect_person(self, frame):
        results = self.model(frame, verbose=False)
        detections = []
        for r in results:
            boxes = r.boxes.xyxy.cpu().numpy()
            names = r.names
            for i, box in enumerate(boxes):
                detections.append({'bbox': box, 'name': names[i]})

        for det in detections:
            if det['name'] == 'person':
                x1, y1, x2, y2 = det['bbox']
                com_x = int((x1 + x2) / 2)
                com_y = int((y1 + y2) / 2)
                return com_x, com_y
        return None, None
