import customtkinter as ctk 
from tkinter import Canvas
from PIL import Image, ImageSequence, ImageTk
import math
import re
after_id=None
import sys
import os
ctk.set_appearance_mode('dark')
def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE = 0x10
def load_font(font_path):
    windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)

load_font(get_path("Syncopate-Regular.ttf"))
load_font(get_path("SpaceX.ttf"))

#niw the code starts
main_window= ctk.CTk()
main_window.title('SnapLink - Main Menu')
main_window.geometry('800x300')

def clear(canvas, canvas_img):
    for item in canvas.find_all():
        if item != canvas_img:
            canvas.delete(item)

def abstract_bg(): 
    global after_id                     #BG CANVAS VERSION
    if after_id:
        main_window.after_cancel(after_id)
    for widget in main_window.winfo_children():
        widget.destroy()
    
    frames = []
    gif = Image.open(get_path("bgminimal.gif"))
    for frame in ImageSequence.Iterator(gif):
        frame = frame.copy().convert("RGBA")
        r, g, b, a = frame.split()
        a = a.point(lambda x: x * 0.4)
        frame.putalpha(a)
        frames.append(ImageTk.PhotoImage(frame.resize((800, 300))))  

    canvas = Canvas(main_window, width=800, height=300, highlightthickness=0, bd=0, bg="black")  
    canvas.place(x=0, y=0)
    canvasbg = canvas.create_image(0, 0, anchor="nw")  

    def animate(frame_index=0):
        global after_id
        canvas.itemconfig(canvasbg, image=frames[frame_index])
        canvas._frames = frames  
        after_id = main_window.after(20, animate, (frame_index + 1) % len(frames))
    animate()

    return canvas, canvasbg

def snaplink_start_menu():
    canvas, canvasbg = abstract_bg()
    canvas.create_text(400, 150, text="SNAPLINK", font=('SpaceX', 33), fill="#ffffff", anchor="center")
    continue_text = canvas.create_text (400, 250, text="Continue", font=('Syncopate', 13), fill="#ffffff", anchor="center")
    canvas.tag_bind(continue_text, "<Button-1>", lambda e: clear(canvas, canvasbg))
    canvas.tag_bind(continue_text, "<Enter>", lambda e: canvas.itemconfig(continue_text, fill="#5C5959"))
    canvas.tag_bind(continue_text, "<Leave>", lambda e: canvas.itemconfig(continue_text, fill="#ffffff"))

snaplink_start_menu()
main_window.mainloop()

