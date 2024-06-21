import customtkinter as ctk
from tkinter import StringVar, IntVar, messagebox
from tkcalendar import Calendar
import os
import sys

# Figure out where the program is running from
exe_dir = os.path.dirname(sys.argv[0])

# Create the path to the activities.txt file in the same folder as the program
activities_file = os.path.join(exe_dir, "activities.txt")

# Function to save the activity details to a file
def save_activity(date, name, length, completed, parent):
    # Mark activity as complete or not
    status = "n" if not completed else "c"
    # Open the file in append mode and add the activity details
    with open(activities_file, "a") as file:
        file.write(f"{date},{name},{length},{status}\n")
    # Bring the window to the front and show a message saying the activity was saved
    parent.lift()
    parent.attributes('-topmost', 1)
    messagebox.showinfo("Saved", "Activity saved successfully!", parent=parent)
    parent.attributes('-topmost', 0)

# Function to read activities from the file
def read_activities():
    activities = []
    # Check if the file exists before trying to read it
    if os.path.exists(activities_file):
        # Open the file in read mode and read all the lines
        with open(activities_file, "r") as file:
            for line in file:
                date, name, length, status = line.strip().split(',')
                activities.append((date, name, length, status))
    return activities

# Function to update and save activity details in the file
def update_activity(date, name, length, status):
    updated_activities = []
    activities = read_activities()

    # Go through each activity and update the one that matches the given date and name
    for activity in activities:
        if (activity[0], activity[1]) == (date, name):
            updated_activities.append((date, name, length, status))
        else:
            updated_activities.append(activity)

    # Write the updated list of activities back to the file
    with open(activities_file, "w") as file:
        for date, name, length, status in updated_activities:
            file.write(f"{date},{name},{length},{status}\n")

# Function to open the Plan page in a new window
def open_plan_page():
    plan_window = ctk.CTkToplevel()
    plan_window.title("Plan Page")
    plan_window.geometry("1000x800")  # Set the size of the window

    # Create a frame for input fields on the left side
    input_frame = ctk.CTkFrame(plan_window)
    input_frame.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")

    # Create a frame for the calendar on the right side
    calendar_frame = ctk.CTkFrame(plan_window)
    calendar_frame.grid(row=0, column=1, padx=40, pady=40, sticky="nsew")

    plan_window.grid_columnconfigure(0, weight=1)
    plan_window.grid_columnconfigure(1, weight=2)
    plan_window.grid_rowconfigure(0, weight=1)

    def save_details():
        date = cal.get_date()
        name = name_var.get()
        length = length_var.get()
        # Check if both name and length are provided before saving
        if not name or not length:
            messagebox.showwarning("Input Error", "Please enter both name and length of the activity.", parent=plan_window)
        else:
            save_activity(date, name, length, False, plan_window)  # Set status as False (not completed) initially

    # Create and add the calendar widget
    cal = Calendar(calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(expand=True, fill="both", padx=40, pady=40)

    name_var = StringVar()
    length_var = IntVar()

    # Create and add input fields and labels
    name_label = ctk.CTkLabel(input_frame, text="Activity Name", font=("Helvetica", 20))
    name_label.pack(pady=20)
    name_entry = ctk.CTkEntry(input_frame, textvariable=name_var, font=("Helvetica", 20))
    name_entry.pack(pady=20, fill="x")

    length_label = ctk.CTkLabel(input_frame, text="Activity Length (minutes)", font=("Helvetica", 20))
    length_label.pack(pady=20)
    length_entry = ctk.CTkEntry(input_frame, textvariable=length_var, font=("Helvetica", 20))
    length_entry.pack(pady=20, fill="x")

    save_button = ctk.CTkButton(input_frame, text="Save Activity", command=save_details, font=("Helvetica", 20))
    save_button.pack(pady=40)

    plan_window.lift()
    plan_window.attributes('-topmost', True)
    plan_window.focus_force()

# Function to open the Track page in a new window
def open_track_page():
    track_window = ctk.CTkToplevel()
    track_window.title("Track Page")
    track_window.geometry("800x600")
    
    track_window.lift()
    track_window.attributes('-topmost', True)
    track_window.focus_force()

    activities = read_activities()
    activity_names = [f"{index} - {date} - {name}" for index, (date, name, length, status) in enumerate(activities)]

    actual_time_var = IntVar()
    completed_var = IntVar()

    def update_selected_activity():
        selected_index = activity_combobox.get()
        # Check if an activity is selected before updating
        if selected_index == "":
            messagebox.showwarning("Selection Error", "Please select an activity to update.", parent=track_window)
            return
        selected_activity = activities[int(selected_index.split(" - ")[0])]
        date, name, original_length, original_status = selected_activity
        actual_time = actual_time_var.get()
        is_completed = completed_var.get()

        updated_status = "c" if is_completed else "n"
        update_activity(date, name, actual_time, updated_status)
        messagebox.showinfo("Updated", f"Activity '{name}' updated successfully!", parent=track_window)

    # Label and dropdown for selecting an activity
    activity_label = ctk.CTkLabel(track_window, text="Select Activity", font=("Helvetica", 16))
    activity_label.pack(pady=20)

    activity_combobox = ctk.CTkOptionMenu(track_window, values=activity_names, font=("Helvetica", 16))
    activity_combobox.pack(pady=10)

    # Entry for the actual time spent on the activity
    actual_time_label = ctk.CTkLabel(track_window, text=f"Actual Time Spent on Selected Activity (minutes)", font=("Helvetica", 16))
    actual_time_label.pack(pady=5)
    actual_time_entry = ctk.CTkEntry(track_window, textvariable=actual_time_var, font=("Helvetica", 16))
    actual_time_entry.pack(pady=5)

    # Checkbox for marking the activity as completed
    completed_checkbox = ctk.CTkSwitch(track_window, text="Completed", variable=completed_var, font=("Helvetica", 16))
    completed_checkbox.pack(pady=10)

    # Button to update the selected activity
    update_button = ctk.CTkButton(track_window, text="Update Activity", command=update_selected_activity, font=("Helvetica", 16))
    update_button.pack(pady=20)

# Function to open the Reports page in a new window
def open_reports_page():
    reports_window = ctk.CTkToplevel()
    reports_window.title("Reports Page")
    reports_window.geometry("600x400")
    reports_label = ctk.CTkLabel(reports_window, text="This is the Reports page", font=("Helvetica", 16))
    reports_label.pack(pady=20, padx=20)
    reports_window.lift()
    reports_window.attributes('-topmost', True)
    reports_window.focus_force()

# Set up the main window
root = ctk.CTk()
root.title("CustomTkinter Application")

# Set the main window size
root.geometry("1200x600")  # Set width and height of the main window

# Create buttons for each panel
plan_button = ctk.CTkButton(root, text="Plan", font=("Helvetica", 16), command=open_plan_page, border_width=2, corner_radius=0)
track_button = ctk.CTkButton(root, text="Track", font=("Helvetica", 16), command=open_track_page, border_width=2, corner_radius=0)
reports_button = ctk.CTkButton(root, text="Reports", font=("Helvetica", 16), command=open_reports_page, border_width=2, corner_radius=0)

# Arrange the buttons horizontally
plan_button.pack(side="left", fill="both", expand=True)
track_button.pack(side="left", fill="both", expand=True)
reports_button.pack(side="left", fill="both", expand=True)

# Start the main loop
root.mainloop()
