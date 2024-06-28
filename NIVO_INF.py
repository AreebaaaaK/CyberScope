import platform
import tkinter as tk
from tkinter import scrolledtext, font, messagebox

def get_system_info():
    my_system = platform.uname()
    info_text.config(state='normal')
    info_text.delete("1.0", 'end')
    info_text.insert('end', f"[INFO] System      : {my_system.system}\n")
    info_text.insert('end', f"[INFO] Node Name   : {my_system.node}\n")
    info_text.insert('end', f"[INFO] Release     : {my_system.release}\n")
    info_text.insert('end', f"[INFO] Version     : {my_system.version}\n")
    info_text.insert('end', f"[INFO] Machine     : {my_system.machine}\n")
    info_text.insert('end', f"[INFO] Processor   : {my_system.processor}\n")
    info_text.config(state='disabled')

def clear_info():
    info_text.config(state='normal')
    info_text.delete("1.0", 'end')
    info_text.config(state='disabled')

# Create main window
root = tk.Tk()
root.title("System Information")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

# Create custom fonts
label_font = font.Font(family="Helvetica Neue", size=12)
text_font = font.Font(family="Courier", size=10)

# Create title
title_label = tk.Label(root, text="System Information", font=("Helvetica Neue", 18, "bold"), bg="#1e1e1e", fg="#ffffff")
title_label.pack(pady=20)

# Create text widget to display results
info_text = scrolledtext.ScrolledText(root, wrap='word', width=80, height=20, bg="#2e2e2e", fg="#ffffff", font=text_font, bd=0, relief="sunken")
info_text.pack(padx=10, pady=10, fill="both", expand=True)

# Button to display system info
info_button = tk.Button(root, text="Get System Info", command=get_system_info, bg="#007acc", fg="#ffffff", font=("Helvetica Neue", 12, "bold"), relief="flat", overrelief="raised", padx=20, pady=10)
info_button.pack(pady=10)

# Button to clear info
clear_button = tk.Button(root, text="Clear Info", command=clear_info, bg="#d70000", fg="#ffffff", font=("Helvetica Neue", 12, "bold"), relief="flat", overrelief="raised", padx=20, pady=10)
clear_button.pack(pady=10)

root.mainloop()
