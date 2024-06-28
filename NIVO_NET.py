import os
import nmap
import tkinter as tk
from tkinter import scrolledtext, messagebox, font

# Function to perform network scan
def perform_scan():
    try:
        scanner = nmap.PortScanner()
        scanner.scan('192.168.0.1/24', arguments='-sn')
        
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END, " Devices Found:\n", 'header')
        
        for host in scanner.all_hosts():
            result_text.insert(tk.END, f"Host: {host} ({scanner[host].hostname()})\n", 'result')
            result_text.insert(tk.END, f"State: {scanner[host].state()}\n", 'result')
            
            for proto in scanner[host].all_protocols():
                result_text.insert(tk.END, f"Protocol: {proto}\n", 'result')
                lport = scanner[host][proto].keys()
                for port in lport:
                    result_text.insert(tk.END, f"Port: {port}\tState: {scanner[host][proto][port]['state']}\n", 'result')
        
        result_text.insert(tk.END, "Network Scan Finished...\n", 'header')
        result_text.config(state=tk.DISABLED)
        result_text.see(tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the scan: {e}")

# Function to clear the results
def clear_results():
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Network Scanner")
root.geometry("900x700")
root.configure(bg="#1c1c1c")

# Create custom fonts
title_font = font.Font(family="Helvetica Neue", size=26, weight="bold")
button_font = font.Font(family="Helvetica Neue", size=14, weight="bold")
text_font = font.Font(family="Courier", size=12)

# Create a frame to hold the title
title_frame = tk.Frame(root, bg="#1c1c1c")
title_frame.pack(pady=20)

# Create and pack the title label
title_label = tk.Label(title_frame, text="Network Scanner", font=title_font, bg="#1c1c1c", fg="#61dafb")
title_label.pack()

# Create a frame to hold the text widget
frame = tk.Frame(root, bg="#1c1c1c")
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Create a scrolled text widget
result_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=100, height=30, bg="#2e2e2e", fg="#dcdcdc", font=text_font, bd=0, relief="sunken")
result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
result_text.config(state=tk.DISABLED)
result_text.tag_config('result', foreground='#dcdcdc')
result_text.tag_config('header', foreground='#61dafb', font=('Courier', 12, 'bold'))

# Create a frame to hold the buttons
button_frame = tk.Frame(root, bg="#1c1c1c")
button_frame.pack(pady=10)

# Create a button to start the scan
scan_button = tk.Button(button_frame, text="Start Scan", command=perform_scan, bg="#007acc", fg="#ffffff", font=button_font, relief="flat", overrelief="raised", padx=20, pady=10)
scan_button.pack(side=tk.LEFT, padx=10)

# Add hover effect to the scan button
def on_enter_scan(e):
    scan_button['background'] = '#005a99'

def on_leave_scan(e):
    scan_button['background'] = '#007acc'

scan_button.bind("<Enter>", on_enter_scan)
scan_button.bind("<Leave>", on_leave_scan)

# Create a button to clear the results
clear_button = tk.Button(button_frame, text="Clear Results", command=clear_results, bg="#ff6f61", fg="#ffffff", font=button_font, relief="flat", overrelief="raised", padx=20, pady=10)
clear_button.pack(side=tk.LEFT, padx=10)

# Add hover effect to the clear button
def on_enter_clear(e):
    clear_button['background'] = '#d55b52'

def on_leave_clear(e):
    clear_button['background'] = '#ff6f61'

clear_button.bind("<Enter>", on_enter_clear)
clear_button.bind("<Leave>", on_leave_clear)

# Start the Tkinter event loop
root.mainloop()
