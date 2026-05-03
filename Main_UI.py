import urllib.request
import urllib.parse
from plyer import notification
from plyer import notification as plyernotification
import json
from zeroconf import Zeroconf, ServiceInfo, ServiceBrowser
selected_device_ip = [None]
received_data = {}
import struct
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
from flask import Flask, send_file as flask_send_file, jsonify
app = Flask(__name__)
shared_files = []
shared_text = [""]
@app.route('/text')
def get_text():
    return jsonify(shared_text[0])
@app.route('/files')
def list_files():
    return jsonify([os.path.basename(f) for f in shared_files])
@app.route('/download/<path:filename>')
def download_file(filename):
    print(f"Looking for: {filename}")
    for f in shared_files:
        print(f"Checking: {f}")
        if os.path.basename(f) == filename:
            return flask_send_file(f, as_attachment=True)
    return "not found", 404
def start_flask():
    app.run(host='0.0.0.0', port=5007, debug=False, use_reloader=False)
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
def startfilepoller(canvas):
    def poll():
        while True:
            devicefilecheck(canvas)
            threading.Event().wait(5)
    threading.Thread(target=poll, daemon=True).start()
def rounded_rect(canvas, x1, y1, x2, y2, r=20, color="white", width=2):
    arc_kwargs = {"outline": color, "width": width}
    line_kwargs = {"fill": color, "width": width}
    canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, style="arc", **arc_kwargs)
    canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, style="arc", **arc_kwargs)
    canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style="arc", **arc_kwargs)          
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
main_window.resizable(False, False)

def clear(canvas, canvas_img):
    for item in canvas.find_all():
        if item != canvas_img:
            canvas.delete(item)
knownfiles ={}
def devicefilecheck(canvas):
    for device in discovered_devices:
        def check(device=device):
            try:
                url = f"http://{device['ip']}:5007/files"
                response = urllib.request.urlopen(url, timeout=2)
                files=set(json.loads(response.read()))
                name = device['name']
                if name not in knownfiles:
                    knownfiles[name] = files
                else:
                    new = files - knownfiles[name]
                    if new:
                        for f in new:
                            main_window.after(0, lambda f=f, n=name: newnotification(canvas, f"{n} shared: {f}"))
                        knownfiles[name] =files
            except:
                pass
        threading.Thread(target=check, daemon=True).start()
def newnotification(canvas, message):
                           x, y, w, h = 400, 150, 210, 80
                           bg= canvas.create_rectangle(x-w//2, y-h//2, x+w//2, y+h//2, fill="#222222", outline="white", width=1)
                           notif = canvas.create_text(x, y, text=message, font=('Syncopate', 10), fill="white", anchor="center", width=180)
                           main_window.after(3000, lambda: canvas.delete(bg))
                           main_window.after(3000, lambda: canvas.delete(notif))
                           threading.Thread(target=lambda: plyernotification.notify(title="Snaplink", message=message, timeout=3), daemon=True).start()
def abstract_bg(): 
    global after_id                                                                                                                                                                          
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
browser_started = False             
pollerstarted = False
def snaplink_main_ui(canvas, canvas_img):
    global browser_started, pollerstarted
    global browser_started
    clear(canvas, canvas_img)
    devicefilecheck(canvas)
    if not pollerstarted:
        startfilepoller(canvas)
        pollerstarted= True
    if not browser_started:
        browserstart(zc, canvas, canvas_img)
        browser_started = True
    update_device_list(canvas, canvas_img)

    canvas.create_text(400, 30, text="SNAPLINK", font=('SpaceX', 21), fill="#ffffff", anchor="center")
    exit_code = canvas.create_text(400, 260, text="Exit", font=('Syncopate', 18), fill="#ffffff", anchor='center')
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
    text_area = ctk.CTkTextbox(canvas, width=175,  height=200, bg_color="#111010", fg_color="#111010",border_color="white",border_width=0,text_color="white",corner_radius=6,font=('Syncopate', 10),wrap="word")
    canvas.create_window(680, 167.5, window=text_area, anchor="center")
    normalimg = Image.open(get_path("fileimg1.png")).resize((230, 230))
    newnormalimg = normalimg.point(lambda p: min(255, int(p * 2.4)))
    hoverimg = newnormalimg.point(lambda p: min(255, int(p * 1 / 1.6)))
    canvas.filepic_img = ImageTk.PhotoImage(newnormalimg)
    canvas.filepic_img_hover = ImageTk.PhotoImage(hoverimg)
    imgitem = canvas.create_image(400, 140, image=canvas.filepic_img, anchor="center")
    refresh = canvas.create_text(400, 288, text="⟳", font=("Syncopate", 17), fill="white", anchor="center")
    canvas.tag_bind(refresh, "<Button-1>", lambda e: snaplink_main_ui(canvas, canvas_img))
    canvas.tag_bind(refresh, "<Enter>", lambda e: canvas.itemconfig(refresh, fill="#5C5959"))
    canvas.tag_bind(refresh, "<Leave>", lambda e: canvas.itemconfig(refresh, fill="#ffffff"))
    canvas.tag_bind(imgitem, "<Enter>", lambda e: canvas.itemconfig(imgitem, image=canvas.filepic_img_hover))
    canvas.tag_bind(imgitem, "<Leave>", lambda e: canvas.itemconfig(imgitem, image=canvas.filepic_img))
    filename_text = canvas.create_text(400, 230, text="No file selected", font=('Syncopate', 8), fill="#aaaaaa", anchor="center")     
    selected_file = [None] # MODIFY THIS LATER
    def textchange(e):
        shared_text[0] = text_area.get("1.0", "end-1c")
    text_area.bind("<KeyRelease>", textchange)
    def pick_file(e):
        from tkinter import filedialog
        main_window.focus_force()
        filepath = filedialog.askopenfilename()
        if filepath:
            selected_file[0] = filepath
            shared_files.clear()
            shared_files.append(filepath)
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
    return ip                                                 
discovered_devices = []
def selfannounce(zc, info):
    zc.register_service(info)
def browserstart(zc, canvas, canvas_img):
    class Snaplinkthing:
        def add_service(self, zc, type_, name):
            info = zc.get_service_info(type_, name)
            if info:
                devicename = info.properties.get(b"name", b"Unknown").decode()
                ip = socket.inet_ntoa(info.addresses[0])
                if devicename not in discovered_devices:
                    discovered_devices.append({"name": devicename, "ip": ip})
                    main_window.after(0, lambda: update_device_list(canvas, canvas_img))
                    main_window.after(0, lambda: newnotification(canvas, f"Device hopped on: {devicename}"))

        def remove_service(self, zc, type_, name):
            info = zc.get_service_info(type_, name)
            if info:
                devicename = info.properties.get(b"name", b"Unknown").decode()
                discovered_devices[:] = [d for d in discovered_devices if d["name"] != devicename]
                main_window.after(0, lambda: update_device_list(canvas, canvas_img))
        def update_service(self, zc, type_, name):
            pass

    ServiceBrowser(zc, "_snaplink._tcp.local.", Snaplinkthing())
def update_device_list(canvas, canvas_img):
    for item in canvas.find_withtag("device"):
        canvas.delete(item)
    for i, device in enumerate(discovered_devices):
        name = device["name"]
        if len(name)>20:
            name = name[:17] + "..."
        displayname=device["name"] if len(device["name"]) <= 18 else device["name"][:15] + "..."
        item = canvas.create_text(110, 90 + i * 25, text=device["name"], font=('Syncopate', 8), fill="#ffffff", anchor="center", tags="device")
        canvas.tag_bind(item, "<Button-1>", lambda e, d=device: newdevice(canvas, canvas_img, d))
        canvas.tag_bind(item, "<Enter>", lambda e, it=item: canvas.itemconfig(it, fill="#5C5959"))
        canvas.tag_bind(item, "<Leave>", lambda e, it=item: canvas.itemconfig(it, fill="#ffffff"))
def newdevice(canvas, canvas_img, device):
    clear(canvas, canvas_img)
    name =device["name"]
    devicefilecheck(canvas)
    if name not in received_data:
        received_data[name] = {"files": [], "texts": []}
    canvas.create_text(400, 30, text=name.upper(), font=('SpaceX', 21), fill="#ffffff", anchor='center' )
    back = canvas.create_text(50, 30, text="BACK", font=('Syncopate', 13), fill="#ffffff", anchor="center")
    canvas.tag_bind(back, "<Button-1>", lambda e: snaplink_main_ui(canvas, canvas_img))
    canvas.tag_bind(back, "<Enter>", lambda e: canvas.itemconfig(back, fill="#5C5959"))
    canvas.tag_bind(back, "<Leave>", lambda e: canvas.itemconfig(back, fill="#ffffff"))
    canvas.create_text(200, 65, text="FILES:", font=('Syncopate', 11), fill="#ffffff", anchor="center")
    rounded_rect(canvas, 20, 80, 380, 270, r=9, color="white", width=2)
    canvas.create_text(600, 65, text="TEXTS:", font=('Syncopate', 11), fill="#ffffff", anchor="center")
    rounded_rect(canvas, 420, 80, 780, 270, r=9, color="white", width=2)
    refresh = canvas.create_text(750, 30, text="⟳", font=("Syncopate", 17), fill="white", anchor="center")
    canvas.tag_bind(refresh, "<Button-1>", lambda e: newdevice(canvas, canvas_img, device))
    canvas.tag_bind(refresh, "<Enter>", lambda e: canvas.itemconfig(refresh, fill="#5C5959"))
    canvas.tag_bind(refresh, "<Leave>", lambda e: canvas.itemconfig(refresh, fill="#ffffff"))
    import urllib.request
    import json
    def load_files():
        try:
            url = f"http://{device['ip']}:5007/files"
            response = urllib.request.urlopen(url, timeout=3)
            files = json.loads(response.read())
            for i, namef in enumerate(files):
                if len(namef) > 25:
                    namefdisplay = namef[:22] + "..."
                else:
                    namefdisplay = namef
                def make_dl(namef, namefdisplay, i):
                    main_window.after(0, lambda: newnotification(canvas, f"New file: {namefdisplay}"))
                    canvas.create_text(40, 100 + i * 25, text=namefdisplay, font=('Syncopate', 12), fill="white", anchor="w", width =300)
                    normal2 = Image.open(get_path("fileimg1.png")).resize((305, 305))
                    normal2bright = normal2.point(lambda p: min(255, int(p * 2.4)))
                    hover2 = normal2bright.point(lambda p: min(255, int(p * 1 / 1.6)))
                    canvas.filepic_img = ImageTk.PhotoImage(normal2bright)
                    canvas.filepic_img_hover = ImageTk.PhotoImage(hover2)
                    imgitem2 = canvas.create_image(200, 188, image=canvas.filepic_img, anchor="center")
                    canvas.tag_bind(imgitem2, "<Enter>", lambda e,: canvas.itemconfig(imgitem2, image=canvas.filepic_img_hover))
                    canvas.tag_bind(imgitem2, "<Leave>",lambda e, : canvas.itemconfig(imgitem2, image=canvas.filepic_img))
                    # dl = canvas.create_text(355, 100 + i * 25, text="DOWNLOAD", font=('Syncopate', 14), fill="#aaaaaa", anchor="center")
                    canvas.tag_bind(imgitem2, "<Button-1>", lambda e, f=namef: downloadfromnewdevice(device['ip'], f))
                    # canvas.tag_bind(dl, "<Enter>", lambda e,: canvas.itemconfig(dl, fill="#ffffff"))
                    # canvas.tag_bind(dl, "<Leave>", lambda e, : canvas.itemconfig(dl, fill="#aaaaaa"))
                main_window.after(0, lambda n=namef, nd=namefdisplay, idx=i: make_dl(n, nd, idx))
        except:
            main_window.after(0, lambda: canvas.create_text(200, 150, text="No files shared", font=('Syncopate', 8), fill="#aaaaaa", anchor="center"))
    threading.Thread(target=load_files, daemon=True).start()
    for i, filepath in enumerate(received_data[name]["files"]):
        namef = os.path.basename(filepath)
        if len(namef) > 35: 
            namef = namef[:22] + "..."
        canvas.create_text(40, 100, + i *25, text=namef, font =('Syncopate', 8), fill="white", anchor="w")
        dl = canvas.create_text(355, 100 + i * 25, text="DL", font=('Syncopate', 8), fill="#aaaaaa", anchor="center")
        canvas.tag_bind(dl, "<Button-1>", lambda e, fp=filepath: os.startfile(os.path.dirname(fp)))
        canvas.tag_bind(dl, "<Enter>", lambda e, d=dl: canvas.itemconfig(d, fill="#ffffff"))
        canvas.tag_bind(dl, "<Leave>", lambda e, d=dl: canvas.itemconfig(d, fill="#aaaaaa"))
        for i, text in enumerate(received_data[name]["texts"]):
            if len (text)  >40:
                text = text[:32] + "..."
            canvas.create_text(430, 100 + i *20, text=text, font = ('Syncopate', 8), fill="#ffffff", anchor="w")
    def loadtext():
        try: 
            url = f"http://{device['ip']}:5007/text"
            response = urllib.request.urlopen(url, timeout=3)
            text = json.loads(response.read())
            main_window.after(0, lambda: canvas.create_text(430, 100, text=text, font =('Syncopate', 8), fill="#aaaaaa", anchor="nw",width =  340))
        except: 
            main_window.after(0, lambda: canvas.create_text(600, 150, text="No text shared", font=('Syncopate', 8), fill="#aaaaaa", anchor="nw"))
    threading.Thread(target=loadtext, daemon=True).start()

def downloadfromnewdevice(ip, filename):
    import urllib.request
    import urllib.parse
    try:
        encoded = urllib.parse.quote(filename)
        url = f"http://{ip}:5007/download/{encoded}"
        savepath = os.path.join(os.path.expanduser("~"), "Downloads", filename)
        print(f"Saving to: {savepath}")
        urllib.request.urlretrieve(url, savepath)
        os.startfile(savepath)
    except Exception as ex:
        print(f"Download error: {ex}")
def select_device(ip, item, canvas):
    selected_device_ip[0] = ip
    for d in canvas.find_withtag("device"):
        canvas.itemconfig(d, fill="#ffffff")
    canvas.itemconfig(item, fill="#5C5959")
def serverfilestart():
    def listen():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', 5006))
        server.listen(5)
        while True: 
            conn, addr = server.accept()
            threading.Thread(target=recievefile, args=(conn,), daemon=True).start()
    threading.Thread(target=listen, daemon=True).start()

def recievefile(conn):
    raw = conn.recv(4)
    filesize = struct.unpack('!I', raw)[0]
    filename_raw = conn.recv(256).decode().strip()
    data = b''
    while len(data) < filesize:
        packet = conn.recv(4096)
        if not packet:
            break
        data +=packet
    savepath = os.path.join(os.path.expanduser("~"), "Downloads", filename_raw)
    with open (savepath, 'wb') as f: 
        f.write(data)
    conn.close()
def sendfile(filepath, target_ip):
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    with open (filepath, 'rb') as f: 
        data = f.read()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_ip, 5006))
    client.send(struct.pack('I', filesize))
    client.send(filename.encode().ljust(256))
    client.send(data)
    client.close()
def networkstart():
    zc = Zeroconf()
    ip = localip()
    info = ServiceInfo( "_snaplink._tcp.local.",f"SnapLink-{socket.gethostname()}._snaplink._tcp.local.", addresses=[socket.inet_aton(ip)],port=5005,properties={"name": socket.gethostname()})
    threading.Thread(target=selfannounce, args=(zc, info), daemon=True).start()
    return zc, info
def snaplink_start_menu():
    canvas, canvasbg = abstract_bg()
    canvas.create_text(400, 135, text="SNAPLINK", font=('SpaceX', 33), fill="#ffffff", anchor="center")
    continue_text_wifi = canvas.create_text (400, 230, text="CONTINUE", font=('Syncopate', 15), fill="#ffffff", anchor="center")
    canvas.tag_bind(continue_text_wifi, "<Button-1>", lambda e: snaplink_main_ui(canvas, canvasbg))
    canvas.tag_bind(continue_text_wifi, "<Enter>", lambda e: canvas.itemconfig(continue_text_wifi, fill="#5C5959"))
    canvas.tag_bind(continue_text_wifi, "<Leave>", lambda e: canvas.itemconfig(continue_text_wifi, fill="#ffffff"))
threading.Thread(target=start_flask, daemon=True).start()
serverfilestart()
zc, info = networkstart()
snaplink_start_menu()
main_window.iconbitmap(get_path("iconsnaplink.ico"))
main_window.mainloop()
