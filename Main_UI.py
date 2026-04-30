from zeroconf import Zeroconf, ServiceInfo, ServiceBrowser
import socket
import threading
import customtkinter as ctk 
from tkinter import Canvas, Text
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

def rounded_rect(canvas, x1, y1, x2, y2, r=20, color="white", width=2):
    arc_kwargs = {"outline": color, "width": width}
    line_kwargs = {"fill": color, "width": width}
    canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, style="arc", **arc_kwargs)
    canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, style="arc", **arc_kwargs)
    canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style="arc", **arc_kwargs)           #ai usage
    canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, style="arc", **arc_kwargs)
    canvas.create_line(x1+r, y1, x2-r, y1, **line_kwargs)
    canvas.create_line(x1+r, y2, x2-r, y2, **line_kwargs)
    canvas.create_line(x1, y1+r, x1, y2-r, **line_kwargs)
    canvas.create_line(x2, y1+r, x2, y2-r, **line_kwargs)
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
def snaplink_main_ui(canvas, canvas_img):                                #MAIN UI CODE HERE
    clear(canvas, canvas_img)
    canvas.create_text(400, 30, text="SNAPLINK", font=('SpaceX', 21), fill="#ffffff", anchor="center")
    exit_code = canvas.create_text(400, 280, text="Exit", font=('Syncopate', 18), fill="#ffffff", anchor='center')
    canvas.tag_bind(exit_code, "<Button-1>", lambda e:main_window.destroy())
    canvas.tag_bind(exit_code, "<Enter>", lambda e: canvas.itemconfig(exit_code, fill="#5C5959"))
    canvas.tag_bind(exit_code, "<Leave>", lambda e: canvas.itemconfig(exit_code, fill="#ffffff"))
    canvas.create_text(110, 45, text="DISCOVERED\nDEVICES:", font=('Syncopate', 13), fill="#ffffff", anchor='center')
    rounded_rect(canvas, 20, 20, 220, 280, r=9, color="white", width=2)
    canvas.create_line((40,70, 185, 70), fill="white", width = 1.6)
    rounded_rect(canvas, 275, 60, 525, 240, r=9, color="white", width=2)
    rounded_rect(canvas, 580, 20, 780, 280, r=9, color="white", width=2)
    canvas.create_text(680, 45, text="SEND TEXT:", font=('Syncopate', 14), fill="#ffffff", anchor='center')
    canvas.create_line((595,60, 765, 60), fill="white", width = 1.6)
    text_area = ctk.CTkTextbox(canvas, width=175,  height=170, bg_color="#111010", fg_color="#111010",border_color="white",border_width=0,text_color="white",corner_radius=6,font=('Syncopate', 10),wrap="word")
    canvas.create_window(680, 157.5, window=text_area, anchor="center")
    submitside = canvas.create_text(680, 265, text="SUBMIT", font=('Syncopate', 13), fill="#ffffff", anchor='center')           
    canvas.tag_bind(submitside, "<Button-1>", lambda e: snaplink_main_ui(canvas, canvas_img))
    canvas.tag_bind(submitside, "<Enter>", lambda e: canvas.itemconfig(submitside, fill="#5C5959"))
    canvas.tag_bind(submitside, "<Leave>", lambda e: canvas.itemconfig(submitside, fill="#ffffff"))
    normalimg = Image.open(get_path("fileimg1.png")).resize((230, 230))
    newnormalimg = normalimg.point(lambda p: min(255, int(p * 2.4)))
    hoverimg = newnormalimg.point(lambda p: min(255, int(p * 1 / 1.6)))
    canvas.filepic_img = ImageTk.PhotoImage(newnormalimg)
    canvas.filepic_img_hover = ImageTk.PhotoImage(hoverimg)
    imgitem = canvas.create_image(400, 140, image=canvas.filepic_img, anchor="center")
    canvas.tag_bind(imgitem, "<Enter>", lambda e: canvas.itemconfig(imgitem, image=canvas.filepic_img_hover))
    canvas.tag_bind(imgitem, "<Leave>", lambda e: canvas.itemconfig(imgitem, image=canvas.filepic_img))
    filename_text = canvas.create_text(400, 230, text="No file selected", font=('Syncopate', 8), fill="#aaaaaa", anchor="center")           #ai usage here btw
    selected_file = [None] # MODIFY THIS LATER

    def pick_file(e):
        from tkinter import filedialog
        main_window.focus_force()
        filepath = filedialog.askopenfilename()
        if filepath:
            name = os.path.basename(filepath)
            if len(name) > 30:
                name = name[:27] + "..."
            canvas.itemconfig(filename_text, text=name)
    canvas.tag_bind(imgitem, "<Button-1>", pick_file)

def localip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip                                                  # end ai usage
discovered_devices = []

def selfannounce(zc, info):
    zc.register_service(info)

def browserstart(zc, canvas):
    class Snaplinkthing:
        def addservice(self, zc, type_, name):
            info = zc.get_service_info(type_, name)
            if info:
                devicename = info.properties.get(b"name", b"Unknown").decode()
                if devicename not in discovered_devices:
                    discovered_devices.append(devicename)
                    main_window.after(0, lambda: update_device_list(canvas))
        def removeservice(self, zc, type_, name):
            pass

        def update_service(self, zc, type_, name):
            pass
    ServiceBrowser(zc, "_snaplink._tcp.local.", Snaplinkthing())
def update_device_list(canvas):
    for item in canvas.find_withtag("device"):
        canvas.delete(item)
    for i, device in enumerate(discovered_devices):
        canvas.create_text(110, 90 + i * 25, text=device, font=('Syncopate', 8), fill="#ffffff", anchor="center", tags="device")
def networkstart():
    zc = Zeroconf()
    ip = localip()
    info = ServiceInfo( "_snaplink._tcp.local.",f"SnapLink-{socket.gethostname()}._snaplink._tcp.local.", addresses=[socket.inet_aton(ip)],port=5005,properties={"name": socket.gethostname()})
    threading.Thread(target=selfannounce, args=(zc, info), daemon=True).start()
    return zc, info
def snaplink_start_menu():
    canvas, canvasbg = abstract_bg()
    canvas.create_text(400, 150, text="SNAPLINK", font=('SpaceX', 33), fill="#ffffff", anchor="center")
    continue_text = canvas.create_text (400, 250, text="Continue", font=('Syncopate', 13), fill="#ffffff", anchor="center")
    canvas.tag_bind(continue_text, "<Button-1>", lambda e: snaplink_main_ui(canvas, canvasbg))
    canvas.tag_bind(continue_text, "<Enter>", lambda e: canvas.itemconfig(continue_text, fill="#5C5959"))
    canvas.tag_bind(continue_text, "<Leave>", lambda e: canvas.itemconfig(continue_text, fill="#ffffff"))
zc, info = networkstart()
snaplink_start_menu()
main_window.mainloop()