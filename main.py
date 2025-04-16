import os
import sys
import platform
import customtkinter as ctk
from datetime import datetime, timedelta

# Initialize customtkinter
ctk.set_appearance_mode("System")  # or "Dark", "Light"
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.title("System Shutdown Scheduler")
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

icon_path = os.path.join(base_path, "assets", "icon.ico")
app.iconbitmap(icon_path)
app.resizable(False, False)
app.geometry("350x380")

# Font settings
font_main = ("Segoe UI", 16)
font_secondary = ("Segoe UI", 14)

# Action selection (Radio buttons)
action_var = ctk.StringVar(value="shutdown")

radio_shutdown = ctk.CTkRadioButton(app, text="Shutdown", variable=action_var, value="shutdown")
radio_restart = ctk.CTkRadioButton(app, text="Restart", variable=action_var, value="restart")
radio_hibernate = ctk.CTkRadioButton(app, text="Hibernate", variable=action_var, value="hibernate")

radio_shutdown.pack(pady=(20, 0))
radio_restart.pack(pady=5)
radio_hibernate.pack(pady=(0, 20))

# Time Picker (Hour and Minute)
time_label = ctk.CTkLabel(app, text="Set time for action:", font=font_main)
time_label.pack()

frame_time = ctk.CTkFrame(app)
frame_time.pack(pady=10)

current_hour = datetime.now().hour
current_minute = datetime.now().minute

hour_var = ctk.StringVar(value=f"{current_hour:02}")
minute_var = ctk.StringVar(value=f"{(current_minute + 1) % 60:02}")

hour_picker = ctk.CTkComboBox(frame_time, width=80, variable=hour_var, values=[f"{i:02}" for i in range(24)])
minute_picker = ctk.CTkComboBox(frame_time, width=80, variable=minute_var, values=[f"{i:02}" for i in range(60)])

hour_picker.pack(side="left", padx=5)
minute_picker.pack(side="left", padx=5)

# Success message label
success_label = ctk.CTkLabel(app, text="", font=font_secondary, text_color="green")
success_label.pack(pady=10)

# Schedule action function
def schedule_action():
    target_time = datetime.now().replace(second=0, microsecond=0)
    selected_hour = int(hour_var.get())
    selected_minute = int(minute_var.get())
    target_time = target_time.replace(hour=selected_hour, minute=selected_minute)

    if target_time <= datetime.now():
        target_time += timedelta(days=1)  # Next day if time already passed

    delay_seconds = int((target_time - datetime.now()).total_seconds())
    action = action_var.get()
    system = platform.system()

    if system == "Windows":
        if action == "shutdown":
            os.system(f"shutdown /s /t {delay_seconds}")
        elif action == "restart":
            os.system(f"shutdown /r /t {delay_seconds}")
        elif action == "hibernate":
            os.system(f"shutdown /h")
    elif system == "Linux":
        delay_minutes = delay_seconds // 60
        if action == "shutdown":
            os.system(f"shutdown -h +{delay_minutes}")
        elif action == "restart":
            os.system(f"shutdown -r +{delay_minutes}")
        elif action == "hibernate":
            os.system("systemctl hibernate")
    else:
        success_label.configure(text="Unsupported OS")
        return

    success_label.configure(text=f"{action.capitalize()} scheduled for {hour_var.get()}:{minute_var.get()}")

def clear_schedule():

    system = platform.system()

    if system == "Windows":
        # Clear the scheduled action (if any)
        os.system("shutdown /a")
    elif system == "Linux":
        # Clear the scheduled action (if any)
        os.system("shutdown -c")
    else:
        success_label.configure(text="Unsupported OS")
        return

    success_label.configure(text="Scheduled action cleared.")

# Button to execute
button_action = ctk.CTkButton(app, text="⏲ Set Schedule", command=schedule_action)
button_action.pack(pady=5)

# Button to clear schedule
button_clear = ctk.CTkButton(app, text="❌ Clear Schedule", command=clear_schedule)
button_clear.pack(pady=(10, 0))
button_clear.configure(fg_color="#e75840", text_color="white")
button_clear.bind("<Enter>", lambda e: button_clear.configure(fg_color="darkred", text_color="white"))  # Change color on hover
button_clear.bind("<Leave>", lambda e: button_clear.configure(fg_color="#e75840", text_color="white"))  # Reset color on leave

# Button for GitHub link
github_link = ctk.CTkButton(app, text="ℹ", command=lambda: os.system("start https://github.com/MehdiSlr/Shutdown-Scheduler"))
github_link.pack(side="right", anchor="sw", padx=10, pady=10)
github_link.configure(width=30, height=30, fg_color="gray", text_color="white")
github_link.bind("<Enter>", lambda e: github_link.configure(fg_color="lightblue", text_color="black"))  # Change color on hover
github_link.bind("<Leave>", lambda e: github_link.configure(fg_color="gray", text_color="white"))  # Reset color on leave

# Run the app
app.mainloop()
