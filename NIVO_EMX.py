import tkinter as tk
from tkinter import scrolledtext, font, messagebox
from bs4 import BeautifulSoup
import requests
import re

class bcolors:
    OK = '\033[92m'
    WA = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'

def extract_emails(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        email_matches = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
        return email_matches
    except requests.RequestException as e:
        return []

def start_extraction():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    emails = extract_emails(url)
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    if emails:
        for email in emails:
            output_text.insert(tk.END, f"{email}\n")
    else:
        output_text.insert(tk.END, "No email found\n")
    output_text.config(state='disabled')

# Create main window
root = tk.Tk()
root.title("NIVOS Email Extractor")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

# Create custom fonts
label_font = font.Font(family="Helvetica Neue", size=12)
text_font = font.Font(family="Courier", size=12)  # Increased font size for output

# Create title label
title_label = tk.Label(root, text="NIVOS Email Extractor", font=("Helvetica Neue", 18, "bold"), bg="#1e1e1e", fg="#ffffff")
title_label.pack(pady=20)

# Create frame for input fields
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(pady=10)

# URL input
url_label = tk.Label(input_frame, text="Please Enter URL:", font=label_font, bg="#1e1e1e", fg="#ffffff")
url_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
url_entry = tk.Entry(input_frame, font=label_font, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Create text widget to display results
output_text = scrolledtext.ScrolledText(root, wrap='word', width=80, height=20, bg="#2e2e2e", fg="#00ff00", font=text_font, bd=0, relief="sunken")  # Changed fg color to green (#00ff00)
output_text.pack(padx=10, pady=10, fill="both", expand=True)

# Button to start extraction
extract_button = tk.Button(root, text="Extract Emails", command=start_extraction, bg="#007acc", fg="#ffffff", font=("Helvetica Neue", 12, "bold"), relief="flat", overrelief="raised", padx=20, pady=10)
extract_button.pack(pady=10)

root.mainloop()
