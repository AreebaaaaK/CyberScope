import os
import time
import tkinter as tk
from tkinter import scrolledtext
from tkinter import font
from scapy.all import ARP, Ether, srp

# Function to clear the text widget
def clear_text_widget():
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    text_widget.config(state=tk.DISABLED)

# Function to print text to the text widget
def print_to_text_widget(message, tag=None):
    text_widget.config(state=tk.NORMAL)
    if tag:
        text_widget.insert(tk.END, message, tag)
    else:
        text_widget.insert(tk.END, message)
    text_widget.config(state=tk.DISABLED)
    text_widget.see(tk.END)

# Function to run the network scan
def scan_network():
    clear_text_widget()
    print_to_text_widget("This Tool Created By AreebaaaaK\n", "hack_")
    print_to_text_widget("\n")
    print_to_text_widget("Starting...\n", "info")
    time.sleep(1)

    # Update the ip variable based on your network segment
    ip_wifi = "192.168.0.1/24"
    ip_ethernet = "192.168.56.1/24"

    # Choose the appropriate ip variable based on your network configuration
    ip = ip_wifi

    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]
    devices = []

    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    print_to_text_widget("Searching Devices...\n", "info")
    time.sleep(3)
    print_to_text_widget("\n")
    print_to_text_widget("IP Address          MAC Address\n", "header")
    print_to_text_widget("="*30 + "\n", "header")
    for i in devices:
        print_to_text_widget("{:16}    {}\n".format(i['ip'], i['mac']), "device")

    print_to_text_widget("\n")
    print_to_text_widget("Finished...\n", "info")

# Initialize the main window
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

# Create a frame to hold the text widget and button
frame = tk.Frame(root, bg="#1c1c1c")
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Create a scrolled text widget
text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=25, bg="#2e2e2e", fg="#dcdcdc", font=text_font, bd=0, relief="sunken")
text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
text_widget.config(state=tk.DISABLED)

# Tag configurations for text widget
text_widget.tag_config("error", foreground="#ff4d4d")
text_widget.tag_config("info", foreground="#61dafb")
text_widget.tag_config("header", foreground="#dcdcdc", font=("Courier", 12, "bold"))
text_widget.tag_config("device", foreground="#9cdcfe")

# Create a frame to hold the buttons
button_frame = tk.Frame(root, bg="#1c1c1c")
button_frame.pack(pady=10)

# Create a button to start the scan
scan_button = tk.Button(button_frame, text="Start Scan", command=scan_network, bg="#007acc", fg="#ffffff", font=button_font, relief="flat", overrelief="raised", padx=20, pady=10)
scan_button.pack(side=tk.LEFT, padx=10)

# Add hover effect to the scan button
def on_enter_scan(e):
    scan_button['background'] = '#005a99'

def on_leave_scan(e):
    scan_button['background'] = '#007acc'

scan_button.bind("<Enter>", on_enter_scan)
scan_button.bind("<Leave>", on_leave_scan)

# Create a button to clear the results
clear_button = tk.Button(button_frame, text="Clear Results", command=clear_text_widget, bg="#ff6f61", fg="#ffffff", font=button_font, relief="flat", overrelief="raised", padx=20, pady=10)
clear_button.pack(side=tk.LEFT, padx=10)

# Add hover effect to the clear button
def on_enter_clear(e):
    clear_button['background'] = '#d55b52'

def on_leave_clear(e):
    clear_button['background'] = '#ff6f61'

clear_button.bind("<Enter>", on_enter_clear)
clear_button.bind("<Leave>", on_leave_clear)

# Run the main loop
root.mainloop()
