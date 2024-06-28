import tkinter as tk
from PIL import Image, ImageTk, ImageOps, ImageDraw
import os

# Function to execute a command
def run_command(command):
    os.system(command)

# Command functions
def command_1(): run_command("sudo python3 ./nivo/NIVO_IP.py")
def command_2(): run_command("sudo python3 ./nivo/NIVO_NET.py")
def command_3(): run_command("sudo python3 ./nivo/NIVO_WEB.py")
def command_4(): run_command("sudo python3 ./nivo/NIVO_DOS.py")
def command_5(): run_command("sudo python3 ./nivo/NIVO_PH.py")
def command_6(): run_command("sudo python3 ./nivo/NIVO_INF.py")
def command_7(): run_command("sudo python3 ./nivo/NIVO_IPF.py")
def command_8(): run_command("sudo python3 ./nivo/NIVO_SQL.py")
def command_9(): run_command("sudo python3 ./nivo/NIVO_XSS.py")
def command_10(): run_command("sudo python3 ./nivo/NIVO_EMX.py")
def command_11(): run_command("sudo python3 ./nivo/NIVO_PG.py")
def command_Q(): root.quit()

# Initialize the main window
root = tk.Tk()
root.title("CyberScope")
root.geometry("850x850")
root.configure(bg="#0d1b2a")

# Load and process the profile image using Pillow
try:
    profile_image_path = "hp.jpg"
    profile_image = Image.open(profile_image_path).resize((100, 100))
    mask = Image.new('L', profile_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + profile_image.size, fill=255)
    profile_image = ImageOps.fit(profile_image, mask.size, centering=(0.5, 0.5))
    profile_image.putalpha(mask)
    profile_photo = ImageTk.PhotoImage(profile_image)
except Exception as e:
    print(f"Error: {e}")
    profile_photo = None

# Create a label for the profile image
profile_label = tk.Label(root, image=profile_photo, bg="#0d1b2a")
profile_label.pack(pady=20)

# Create a label for the name
name_label = tk.Label(root, text="CyberScope", font=("Helvetica", 24, "bold"), bg="#0d1b2a", fg="#ffffff")
name_label.pack(pady=10)

# Create a frame for the buttons
button_frame = tk.Frame(root, bg="#0b132b")
button_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Create and place the buttons in two columns
button_texts = [
    "1. Scan Devices In Your Network",
    "2. Scan Networks",
    "3. Scan Website [NMAP, WHOIS]",
    "4. DOS-DDOS",
    "5. Phone [Information Gathering, SMS Sender]",
    "6. Get Your Information [System INFO]",
    "7. IP [Information Gathering]",
    "8. SQL Scan (WEBSITE)",
    "9. XSS Vulnerability Scan",
    "10. Email Extractor",
    "11. Password Generator",
    "Q. Quit"
]

commands = [
    command_1, command_2, command_3, command_4, command_5, command_6, command_7, command_8, 
    command_9, command_10, command_11, command_Q
]

button_bg = "#0d1b2a"
button_fg = "#ffffff"
button_active_bg = "#0b132b"

# Place buttons in two columns
midpoint = 10
for i in range(midpoint):
    button = tk.Button(button_frame, text=button_texts[i], command=commands[i], width=40, height=2, bg=button_bg, fg=button_fg, activebackground=button_active_bg, font=("Helvetica Neue", 12, "bold"))
    button.grid(row=i, column=0, padx=10, pady=5, sticky="ew")

for i in range(midpoint, len(button_texts)):
    button = tk.Button(button_frame, text=button_texts[i], command=commands[i], width=40, height=2, bg=button_bg, fg=button_fg, activebackground=button_active_bg, font=("Helvetica Neue", 12, "bold"))
    button.grid(row=i - midpoint, column=1, padx=10, pady=5, sticky="ew")

# Ensure the columns resize properly
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

# Run the main loop
root.mainloop()
