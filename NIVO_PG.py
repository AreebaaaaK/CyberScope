import tkinter as tk
from tkinter import font, messagebox
import string
import random

class bcolors:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'

def generate_password():
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)

    try:
        uzunluq = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for password length.")
        return

    password = []
    for i in range(uzunluq):
        password.append(random.choice(characters))

    random.shuffle(password)

    password_str = "".join(password)
    password_output.config(state='normal')
    password_output.delete("1.0", tk.END)
    password_output.insert(tk.END, password_str)
    password_output.config(state='disabled')

# Create main window
root = tk.Tk()
root.title("NIVOS Password Generator")
root.geometry("600x400")  # Increased width and height
root.configure(bg="#1e1e1e")

# Create custom fonts
label_font = font.Font(family="Helvetica Neue", size=12)
output_font = font.Font(family="Courier", size=16)  # Increased font size for output

# Title label
title_label = tk.Label(root, text="NIVOS Password Generator", font=("Helvetica Neue", 18, "bold"), bg="#1e1e1e", fg="#ffffff")
title_label.pack(pady=20)

# Frame for input and output
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(pady=10)

# Password length input
length_label = tk.Label(input_frame, text="Enter password length:", font=label_font, bg="#1e1e1e", fg="#ffffff")
length_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
length_entry = tk.Entry(input_frame, font=label_font, width=10)
length_entry.grid(row=0, column=1, padx=5, pady=5)

# Button to generate password
generate_button = tk.Button(root, text="Generate Password", command=generate_password, bg="#007acc", fg="#ffffff", font=("Helvetica Neue", 12, "bold"), relief="flat", overrelief="raised", padx=20, pady=10)
generate_button.pack(pady=10)

# Output text widget to display generated password
password_output = tk.Text(root, wrap='word', width=60, height=15, bg="#2e2e2e", fg="#ffffff", font=output_font, bd=0, relief="sunken")
password_output.pack(padx=10, pady=10)

root.mainloop()
