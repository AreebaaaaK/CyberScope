import requests
import sys
import os
import tkinter as tk
from tkinter import scrolledtext, font, messagebox

class bcolors:
    OK = '\033[92m' 
    WARNING = '\033[93m' 
    FAIL = '\033[91m' 
    RESET = '\033[0m'

def locate():
    ip = ip_entry.get()
    if not ip:
        messagebox.showerror("Error", "Please enter an IP address.")
        return

    try:
        data = requests.get("http://ip-api.com/json/" + ip + "?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,currency,isp,as,mobile,proxy")
        resp = data.json()
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Request failed: {e}")
        return

    info_text.config(state='normal')
    info_text.delete("1.0", 'end')
    
    info_text.insert('end', f"[INFO] Results :\n\n")
    info_text.insert('end', "Status : " + resp["status"] + "\n")
    if resp["status"] == "fail":
        info_text.insert('end', "Fail : " + resp["message"] + "\n")
        info_text.config(state='disabled')
        return
    
    info_text.insert('end', "Continent: " + resp["continent"] + "\n")
    info_text.insert('end', "Country Code     : " + resp["continentCode"] + "\n")
    info_text.insert('end', "Country          : " + resp["country"] + "\n")
    info_text.insert('end', "Country Code     : " + resp["countryCode"] + "\n")
    info_text.insert('end', "Region           : " + resp["region"] + "\n")
    info_text.insert('end', "Region Number    : " + resp["regionName"] + "\n")
    info_text.insert('end', "City             : " + resp["city"] + "\n")
    info_text.insert('end', "District         : " + resp["district"] + "\n")
    info_text.insert('end', "Postal Code      : " + resp["zip"] + "\n")
    info_text.insert('end', "Latitude         : " + str(resp["lat"]) + "\n")
    info_text.insert('end', "Longitude        : " + str(resp["lon"]) + "\n")
    info_text.insert('end', "Timezone         : " + resp["timezone"] + "\n")
    info_text.insert('end', "Operator         : " + resp["isp"] + "\n")
    info_text.insert('end', "AS               : " + resp["as"] + "\n")
    info_text.insert('end', "Mobile           : " + str(resp["mobile"]) + "\n")
    info_text.insert('end', "Proxy            : " + str(resp["proxy"]) + "\n")
    
    info_text.config(state='disabled')

def clear_output():
    info_text.config(state='normal')
    info_text.delete("1.0", 'end')
    info_text.config(state='disabled')

# Create main window
root = tk.Tk()
root.title("IP Tracker")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

# Create custom fonts
label_font = font.Font(family="Helvetica Neue", size=12)
text_font = font.Font(family="Courier", size=10)

# Create title
title_label = tk.Label(root, text="IP Tracker", font=("Helvetica Neue", 18, "bold"), bg="#1e1e1e", fg="#ffffff")
title_label.pack(pady=20)

# Create frame for input fields
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(pady=10)

# IP address input
ip_label = tk.Label(input_frame, text="Input IP:", font=label_font, bg="#1e1e1e", fg="#ffffff")
ip_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
ip_entry = tk.Entry(input_frame, font=label_font, width=30)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

# Create text widget to display results
info_text = scrolledtext.ScrolledText(root, wrap='word', width=80, height=20, bg="#2e2e2e", fg="#ffffff", font=text_font, bd=0, relief="sunken")
info_text.pack(padx=10, pady=10, fill="both", expand=True)

# Button to locate IP
locate_button = tk.Button(root, text="Locate IP", command=locate, bg="#007acc", fg="#ffffff", font=("Helvetica Neue", 12, "bold"), relief="flat", overrelief="raised", padx=20, pady=10)
locate_button.pack(pady=10)

# Button to clear text
clear_button = tk.Button(root, text="Clear Output", command=clear_output, bg="#007acc", fg="#ffffff", font=("Helvetica Neue", 12, "bold"), relief="flat", overrelief="raised", padx=20, pady=10)
clear_button.pack(pady=10)

root.mainloop()
