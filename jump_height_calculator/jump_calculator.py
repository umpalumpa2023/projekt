# jump_calculator.py

from datetime import datetime
import cv2
from tkinter import messagebox

class JumpHeightCalculator:
    def __init__(self):
        self.lowest_com_y = float('inf')
        self.highest_com_y = 0
        self.jump_heights = []
        self.all_jumps = []
        self.in_air = False
        self.jump_frames = []

    def update_com_position(self, com_y):
        if com_y < self.lowest_com_y:
            self.lowest_com_y = com_y
            if not self.in_air:
                self.in_air = True
        if com_y > self.highest_com_y and self.in_air:
            self.highest_com_y = com_y

    def calculate_jump_height(self, pixel_to_cm_ratio=1):
        height = (self.highest_com_y - self.lowest_com_y) * pixel_to_cm_ratio
        return max(height, 0)

    def reset(self):
        self.lowest_com_y = float('inf')
        self.highest_com_y = 0
        self.in_air = False
        self.jump_frames = []

    def store_jump_height(self, jump_height):
        self.jump_heights.append(jump_height)
        if len(self.jump_heights) > 3:
            self.jump_heights.pop(0)
        jump_record = {
            "height": jump_height,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "frames": self.jump_frames.copy()
        }
        self.all_jumps.append(jump_record)

    def get_jump_history(self):
        return self.all_jumps

    def save_jump_to_file(self, jump_data, filename):
        if not jump_data['frames']:
            messagebox.showerror("Error", "No frames recorded for this jump.")
            return
        height, width, _ = jump_data['frames'][0].shape
        out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 20, (width, height))
        for frame in jump_data['frames']:
            out.write(frame)
        out.release()
        messagebox.showinfo("Success", f"Jump saved to {filename}")
