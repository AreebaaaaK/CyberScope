import socket
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, font
from colorama import Fore, Style

class bcolors:
    OK = Fore.GREEN
    WARNING = Fore.YELLOW
    FAIL = Fore.RED
    RESET = Style.RESET_ALL

def resolve_ip(url):
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]
    domain = url.split('/')[0]
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None

def perform_nmap(options, ip):
    command = f"sudo nmap {options} {ip}"
    process = os.popen(command)
    results = process.read()
    process.close()
    return results

def perform_whois(url):
    command = f'sudo whois {url}'
    process = os.popen(command)
    results = process.read()
    process.close()
    if not results.strip():
        return f"{bcolors.FAIL}No Data Found{bcolors.RESET}"
    return results

def start_scan():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "No URL provided.")
        return

    ip_address = resolve_ip(url)
    if ip_address is None:
        messagebox.showerror("Error", "Failed to resolve URL to IP address.")
        return

    option = scan_option.get()
    if option == '1':
        result = perform_nmap("-F", ip_address)
    elif option == '2':
        result = perform_whois(url)
    elif option == '3':
        result = f"{bcolors.WARNING}[INFO] 1. Scan\n"
        result += os.popen(f"sudo nmap -sV {ip_address}").read()
        port = port_entry.get().strip()
        if port.isdigit():
            result += os.popen(f"sudo nmap -Pn --script vuln {ip_address} -p {port}").read()
        else:
            messagebox.showerror("Error", "Invalid port number.")
            return
    else:
        result = f"{bcolors.WARNING}[WARNING] Invalid Command Detected. Please Input Valid Commands."

    result_text.config(state=tk.NORMAL)
    result_text.insert(tk.END, result, 'result')
    result_text.config(state=tk.DISABLED)
    result_text.see(tk.END)

def clear_results():
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Website Scanner")
root.geometry("800x600")
root.configure(bg="#1c1c1c")

# Create custom fonts
title_font = font.Font(family="Helvetica Neue", size=24, weight="bold")
button_font = font.Font(family="Helvetica Neue", size=12, weight="bold")
text_font = font.Font(family="Courier", size=10)

# Create a frame to hold the title
title_frame = tk.Frame(root, bg="#1c1c1c")
title_frame.pack(pady=10)

# Create and pack the title label
title_label = tk.Label(title_frame, text="Website Scanner", font=title_font, bg="#1c1c1c", fg="#61dafb")
title_label.pack()

# Create a frame to hold the URL entry and scan options
input_frame = tk.Frame(root, bg="#1c1c1c")
input_frame.pack(pady=10)

# Create and pack the URL entry
url_label = tk.Label(input_frame, text="URL:", font=button_font, bg="#1c1c1c", fg="#ffffff")
url_label.grid(row=0, column=0, padx=10, pady=5)
url_entry = tk.Entry(input_frame, font=text_font, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5)

# Create and pack the scan options
option_label = tk.Label(input_frame, text="Scan Option:", font=button_font, bg="#1c1c1c", fg="#ffffff")
option_label.grid(row=1, column=0, padx=10, pady=5)
scan_option = tk.StringVar()
scan_option.set('1')
options = [("NMAP INFO Scan", '1'), ("Whois Scan", '2'), ("NMAP Vulnerabilities Scan", '3')]
for i, (text, value) in enumerate(options):
    tk.Radiobutton(input_frame, text=text, variable=scan_option, value=value, font=button_font, bg="#1c1c1c", fg="#ffffff", selectcolor="#1c1c1c").grid(row=1, column=i+1, padx=10, pady=5)

# Create and pack the port entry for vulnerabilities scan
port_label = tk.Label(input_frame, text="Open Port:", font=button_font, bg="#1c1c1c", fg="#ffffff")
port_label.grid(row=2, column=0, padx=10, pady=5)
port_entry = tk.Entry(input_frame, font=text_font, width=20)
port_entry.grid(row=2, column=1, padx=10, pady=5)

# Create a frame to hold the text widget
frame = tk.Frame(root, bg="#1c1c1c")
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Create a scrolled text widget
result_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=100, height=15, bg="#2e2e2e", fg="#dcdcdc", font=text_font, bd=0, relief="sunken")
result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
result_text.config(state=tk.DISABLED)
result_text.tag_config('result', foreground='#dcdcdc')
result_text.tag_config('header', foreground='#61dafb', font=('Courier', 12, 'bold'))

# Create a frame to hold the buttons
button_frame = tk.Frame(root, bg="#1c1c1c")
button_frame.pack(pady=10)

# Create a button to start the scan
scan_button = tk.Button(button_frame, text="Start Scan", command=start_scan, bg="#007acc", fg="#ffffff", font=button_font, relief="flat", overrelief="raised", padx=20, pady=10)
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
