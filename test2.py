import customtkinter as ctk
from tkinter import filedialog
import socket

def send_file():
    # Pick the file using CTK/Tkinter
    path = filedialog.askopenfilename()
    if not path: return

    # Connect to the receiver
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5001)) # Connect to local computer

    # Send the bits
    with open(path, "rb") as f:
        data = f.read(1024)
        while data:
            client.send(data)
            data = f.read(1024)
            
    client.close()
    print("Sent!")

# Simple CTK UI
app = ctk.CTk()
btn = ctk.CTkButton(app, text="Select & Send File", command=send_file)
btn.pack(pady=20, padx=20)
app.mainloop()
