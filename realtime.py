import time
import pyautogui
import pygetwindow as gw
from ultralytics import YOLO
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2

model = YOLO(model='yolov8n-MC-1.20.6.pt')
root, label = None, None


def capAndPred():
    global root, label
    window = gw.getActiveWindow()
    if window is None:
        root.after(1, capAndPred)
        return
    x, y, width, height = window.left, window.top, window.width, window.height
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    results = model.predict(source=screenshot, save=False,
                            imgsz=1920, stream=False)
    for result in results:
        image_array = result.plot()
        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        new_image = Image.fromarray(image_array)
        new_image = new_image.resize((600, 360))
        new_photo = ImageTk.PhotoImage(new_image)
        label.config(image=new_photo)
        label.image = new_photo
        break
    root.after(1, capAndPred)


def main():
    global root, label
    root = tk.Tk()
    root.geometry("600x360+50+50")
    root.title("结果展示")
    image = Image.open("start.png")
    image = image.resize((600, 360))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo)
    label.pack()
    root.after(1000, capAndPred)
    root.mainloop()


if __name__ == "__main__":
    main()

