# main.py

import tkinter as tk
from gui.jump_height_app import JumpHeightApp
from recognition.yolo_recognition import YOLORecognition

def main():
    root = tk.Tk()
    recognition_software = YOLORecognition()
    app = JumpHeightApp(root, recognition_software)
    root.mainloop()

if __name__ == "__main__":
    main()
