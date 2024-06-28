import phonenumbers
from phonenumbers import carrier, geocoder, timezone
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

def get_city_name(description):
    parts = description.split(', ')
    if len(parts) > 1:
        return parts[1]
    return ""

def display_info():
    mobileNo = phone_entry.get()
    if not mobileNo.startswith('+'):
        messagebox.showerror("Error", "Please include the country code (e.g., +91 for India).")
        return
    try:
        mobileNo = phonenumbers.parse(mobileNo)
        country = geocoder.description_for_number(mobileNo, 'en')
        city = get_city_name(country)
        timezone_info = timezone.time_zones_for_number(mobileNo)
        carrier_info = carrier.name_for_number(mobileNo, 'en')
        valid_number = phonenumbers.is_valid_number(mobileNo)
        possible_number = phonenumbers.is_possible_number(mobileNo)

        result_text.config(state='normal')
        result_text.delete("1.0", 'end')
        result_text.insert('end', f"{bcolors.OK}Timezone: {timezone_info}\n{bcolors.RESET}")
        result_text.insert('end', f"{bcolors.OK}Carrier: {carrier_info}\n{bcolors.RESET}")
        result_text.insert('end', f"{bcolors.OK}Location: {country}\n{bcolors.RESET}")
        result_text.insert('end', f"{bcolors.OK}City: {city}\n{bcolors.RESET}")
        result_text.insert('end', f"{bcolors.OK}Valid Mobile Number: {valid_number}\n{bcolors.RESET}")
        result_text.insert('end', f"{bcolors.OK}Possible Number: {possible_number}\n{bcolors.RESET}")
        result_text.see('end')
        result_text.config(state='disabled')

    except phonenumbers.NumberParseException as e:
        messagebox.showerror("Error", str(e))

# Create main window
root = tk.Tk()
root.title("Phone Number Info Tool")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

# Create custom fonts
title_font = font.Font(family="Helvetica Neue", size=18, weight="bold")
label_font = font.Font(family="Helvetica Neue", size=12)
button_font = font.Font(family="Helvetica Neue", size=12, weight="bold")
text_font = font.Font(family="Courier", size=10)

# Create title
title_label = tk.Label(root, text="Phone Number Info Tool", font=title_font, bg="#1e1e1e", fg="#ffffff")
title_label.pack(pady=20)

# Create frame for input fields
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(pady=10)

# Phone number input
phone_label = tk.Label(input_frame, text="Phone Number:", font=label_font, bg="#1e1e1e", fg="#ffffff")
phone_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
phone_entry = tk.Entry(input_frame, font=label_font, width=30)
phone_entry.grid(row=0, column=1, padx=5, pady=5)

# Create text widget to display results
result_text = scrolledtext.ScrolledText(root, wrap='word', width=80, height=20, bg="#2e2e2e", fg="#ffffff", font=text_font, bd=0, relief="sunken")
result_text.pack(padx=10, pady=10, fill="both", expand=True)

# Button to display phone number info
info_button = tk.Button(root, text="Get Info", command=display_info, bg="#007acc", fg="#ffffff", font=button_font, relief="flat", overrelief="raised", padx=20, pady=10)
info_button.pack(pady=10)

# Button to clear results
clear_button = tk.Button(root, text="Clear Results", command=lambda: result_text.delete("1.0", 'end'), bg="#007acc", fg="#ffffff", font=button_font, relief="flat", overrelief="raised", padx=20, pady=10)
clear_button.pack(pady=10)

root.mainloop()
