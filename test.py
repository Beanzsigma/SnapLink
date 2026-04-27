import customtkinter as ctk

def clear_window():
    # This loop removes everything currently on the screen
    for widget in window.winfo_children():
        widget.destroy()

def show_main_menu():
    clear_window()
    
    label = ctk.CTkLabel(window, text="Main Menu", font=("Arial", 20))
    label.pack(pady=20)
    
    # Button to "go" to another interface
    btn = ctk.CTkButton(window, text="Open Settings", command=show_settings)
    btn.pack()

def show_settings():
    clear_window()
    
    label = ctk.CTkLabel(window, text="Settings Interface", font=("Arial", 20))
    label.pack(pady=20)
    
    # Button to "go back"
    btn = ctk.CTkButton(window, text="Back to Menu", command=show_main_menu)
    btn.pack()

window = ctk.CTk()
window.geometry("300x200")

# Start at the main menu
show_main_menu()

window.mainloop()
