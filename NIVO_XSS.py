
import tkinter as tk
from tkinter import scrolledtext, font, messagebox
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import requests
from pprint import pprint

class bcolors:
    OK = '\033[92m' 
    a = '\033[93m' 
    FAIL = '\033[91m'  
    RESET = '\033[0m' 

def get_all_forms(url):
    """Given a `url`, it returns all forms from the HTML content"""
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    """
    This function extracts all possible useful information about an HTML `form`
    """
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, value):
    """
    Submits a form given in `form_details`
    Params:
        form_details (list): a dictionary that contain form information
        url (str): the original URL that contain that form
        value (str): this will be replaced to all text and search inputs
    Returns the HTTP Response after form submission
    """
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value

    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        # GET request
        return requests.get(target_url, params=data)

def scan_xss(url):
    """
    Given a `url`, it prints all XSS vulnerable forms and 
    returns True if any is vulnerable, False otherwise
    """
    forms = get_all_forms(url)
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"[+] Detected {len(forms)} forms on {url}.\n")
    js_script = "<Script>alert('hi')</scripT>"
    is_vulnerable = False
    for form in forms: 
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            output_text.insert(tk.END, f"[+] XSS Detected on {url}\n")
            output_text.insert(tk.END, f"[*] Form details:\n")
            output_text.insert(tk.END, f"{pprint.pformat(form_details)}\n\n")
            is_vulnerable = True
    output_text.config(state='disabled')
    if not is_vulnerable:
        output_text.insert(tk.END, "No XSS vulnerabilities detected.\n")

def start_scan():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return
    scan_xss(url)

# Create main window
root = tk.Tk()
root.title("NIVOS XSS Scanner")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

# Create custom fonts
label_font = font.Font(family="Helvetica Neue", size=12)
text_font = font.Font(family="Courier", size=14, weight="bold")  # Increased font size and made it bold

# Create title label
title_label = tk.Label(root, text="NIVOS XSS Scanner", font=("Helvetica Neue", 18, "bold"), bg="#1e1e1e", fg="#ffffff")
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

# Button to start XSS Scan
scan_button = tk.Button(root, text="Start XSS Scan", command=start_scan, bg="#007acc", fg="#ffffff", font=("Helvetica Neue", 12, "bold"), relief="flat", overrelief="raised", padx=20, pady=10)
scan_button.pack(pady=10)

root.mainloop()

