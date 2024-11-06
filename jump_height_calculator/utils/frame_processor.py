# utils/frame_processor.py

import cv2

def process_frame(frame, jump_height_calculator, recognition_software):
    com_x, com_y = recognition_software.detect_person(frame)
    if com_x and com_y:
        jump_height_calculator.update_com_position(com_y)
        cv2.circle(frame, (com_x, com_y), 10, (255, 0, 0), -1)
    return frame
