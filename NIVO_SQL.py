import tkinter as tk
from tkinter import scrolledtext, font, messagebox
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
import requests
import threading

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

def get_all_forms(url):
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def is_vulnerable(response):
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False

def scan_sql_injection(url):
    output_text.config(state='normal')
    output_text.delete("1.0", 'end')
    
    for c in "\"'":
        new_url = f"{url}{c}"
        output_text.insert('end', f"[!] Trying {new_url}\n")
        res = s.get(new_url)
        if is_vulnerable(res):
            output_text.insert('end', f"[+] SQL Injection vulnerability detected, link: {new_url}\n")
            output_text.config(state='disabled')
            return
    forms = get_all_forms(url)
    output_text.insert('end', f"[+] Detected {len(forms)} forms on {url}.\n")
    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    data[input_tag["name"]] = f"test{c}"
            action_url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = s.post(action_url, data=data)
            elif form_details["method"] == "get":
                res = s.get(action_url, params=data)
            if is_vulnerable(res):
                output_text.insert('end', f"[+] SQL Injection vulnerability detected, link: {action_url}\n")
                output_text.insert('end', f"[+] Form:\n")
                output_text.insert('end', pprint.pformat(form_details, width=40))
                break
    output_text.config(state='disabled')

def start_scan():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return
    threading.Thread(target=scan_sql_injection, args=(url,)).start()

# Create main window
root = tk.Tk()
root.title("NIVOS SQL Injection Tool")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

# Create custom fonts
label_font = font.Font(family="Helvetica Neue", size=12)
text_font = font.Font(family="Courier", size=12, weight="bold")  # Increased font size and made it bold

# Create title
title_label = tk.Label(root, text="NIVOS SQL Injection Tool", font=("Helvetica Neue", 18, "bold"), bg="#1e1e1e", fg="#ffffff")
title_label.pack(pady=20)

# Create frame for input fields
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(pady=10)

# URL input
url_label = tk.Label(input_frame, text="Please Input URL:", font=label_font, bg="#1e1e1e", fg="#ffffff")
url_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
url_entry = tk.Entry(input_frame, font=label_font, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Create text widget to display results
output_text = scrolledtext.ScrolledText(root, wrap='word', width=80, height=20, bg="#2e2e2e", fg="#00ff00", font=text_font, bd=0, relief="sunken")  # Changed fg color to green (#00ff00)
output_text.pack(padx=10, pady=10, fill="both", expand=True)

# Button to start SQL Injection scan
scan_button = tk.Button(root, text="Start Scan", command=start_scan, bg="#007acc", fg="#ffffff", font=("Helvetica Neue", 12, "bold"), relief="flat", overrelief="raised", padx=20, pady=10)
scan_button.pack(pady=10)

root.mainloop()
