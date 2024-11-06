# gui/jump_height_app.py

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
import cv2
from jump_calculator import JumpHeightCalculator
from utils.frame_processor import process_frame

class JumpHeightApp:
    def __init__(self, root, recognition_software):
        self.root = root
        self.root.title("Jump Height Estimation Tool (Live Feed)")
        self.jump_height_calculator = JumpHeightCalculator()
        self.recognition_software = recognition_software
        self.camera_active = False

        self.label = tk.Label(root, text="Live Video Stream: Perform a Jump!")
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_camera)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_camera)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.history_label = tk.Label(root, text="Jump Heights (Last 3): None")
        self.history_label.pack(pady=10)

        self.history_button = tk.Button(root, text="View All Jumps", command=self.show_jump_history)
        self.history_button.pack(pady=5)

        self.replay_button = tk.Button(root, text="Replay Last Jump", command=self.replay_last_jump)
        self.replay_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Last Jump", command=self.save_last_jump)
        self.save_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_history(self):
        heights_text = ', '.join(f'{h:.2f} cm' for h in self.jump_height_calculator.jump_heights)
        self.history_label.config(text=f"Jump Heights (Last 3): {heights_text or 'None'}")

    def start_camera(self):
        if not self.camera_active:
            self.camera_active = True
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Cannot open camera")
                return
            self.update_frame()

    def stop_camera(self):
        if self.camera_active:
            self.camera_active = False
            self.cap.release()

    def update_frame(self):
        if not self.camera_active:
            return

        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture video frame")
            return

        frame = process_frame(frame, self.jump_height_calculator, self.recognition_software)
        self.jump_height_calculator.jump_frames.append(frame.copy())

        if self.jump_height_calculator.in_air and self.jump_height_calculator.lowest_com_y < self.jump_height_calculator.highest_com_y:
            jump_height = self.jump_height_calculator.calculate_jump_height(pixel_to_cm_ratio=0.26)
            if jump_height >= 5:
                self.jump_height_calculator.store_jump_height(jump_height)
                self.update_history()
            self.jump_height_calculator.reset()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(frame_pil)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=frame_tk)
        self.canvas.image = frame_tk

        self.root.after(10, self.update_frame)

    def show_jump_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Jump History")

        tree = ttk.Treeview(history_window, columns=('Height', 'Timestamp'), show='headings')
        tree.heading('Height', text='Jump Height (cm)')
        tree.heading('Timestamp', text='Timestamp')
        tree.pack(fill=tk.BOTH, expand=True)

        for jump in self.jump_height_calculator.get_jump_history():
            tree.insert('', tk.END, values=(f"{jump['height']:.2f} cm", jump['timestamp']))

    def replay_last_jump(self):
        if not self.jump_height_calculator.jump_heights:
            messagebox.showwarning("No Jump", "No jump recorded yet!")
            return

        frames = self.jump_height_calculator.all_jumps[-1]['frames']
        if frames:
            self.replay_video(frames)
        else:
            messagebox.showwarning("No Jump Video", "No frames recorded for the last jump.")

    def replay_video(self, frames):
        for frame in frames:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_tk = ImageTk.PhotoImage(frame_pil)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=frame_tk)
            self.canvas.image = frame_tk
            self.root.update()
            cv2.waitKey(50)

    def save_last_jump(self):
        if not self.jump_height_calculator.jump_heights:
            messagebox.showwarning("No Jump", "No jump recorded yet!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
        if not file_path:
            return

        last_jump_data = self.jump_height_calculator.all_jumps[-1]
        self.jump_height_calculator.save_jump_to_file(last_jump_data, file_path)

    def on_closing(self):
        if self.camera_active:
            self.cap.release()
        self.root.quit()
        self.root.destroy()
