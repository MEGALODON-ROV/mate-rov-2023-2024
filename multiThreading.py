import pygame
import cv2
import sys
import serial
from time import sleep
from threading import Thread
import tkinter as tk
import serial
import queue                
import time



sys.path.append("C://Users//alexa//OneDrive//Documents//GitHub//mate-rov-2023-2024")
import nav_main

globalState = 0

def Gui():
    root = tk.Tk()
    root.title("ROV Control Panel")
    

    #Create a larger canvas
    canvas_width = 300 # Adjust the width as needed
    canvas_height = 150  # Adjust the height as needed
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()


    imgprog2 = tk.Button(root, text="img prog", command=lambda: imgProc())
    imgprog2.place(x=80, y=35)

    startNav = tk.Button(root, text="Start Nav", command=lambda: globals().update(globalState = 1))
    startNav.place(x=200, y=35)

    stop_button = tk.Button(root, text="Stop Nav", command=lambda: globals().update(globalState = 0))
    stop_button.place(x=200, y=65)  

    stop_GUI = tk.Button(root, text="Stop GUI", command=lambda: root.destroy())
    stop_GUI.place(x=150, y=120)

    depth_label = tk.Label(root, text="IMG PROG:")
    depth_label.place(x=80, y=5)

    depth_label = tk.Label(root, text="NAV:")
    depth_label.place(x=200, y=5)
    root.mainloop()

def imgProc():
    print("banana")

def navLoop():
    while globalState == 0:
        sleep(1)
    pygame.init()
    while 1: 
        event = pygame.event.poll()
        if globalState == 1:
            if event.type == pygame.QUIT:
                break
        print("nav loop started")
        nav_main.nav()
        sleep(0.1)
    pygame.quit()
    


if __name__ == '__main__':
    navThread = Thread(target=Gui,)
    navThread.start()
    navLoop()
    

    





