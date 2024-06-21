import customtkinter as ctk  # Importing customtkinter library as ctk
from tkinter import StringVar, IntVar, messagebox  # Importing necessary components from tkinter
from tkcalendar import Calendar  # Importing Calendar widget from tkcalendar
import os  # Importing os module for operating system functionalities
import sys  # Importing sys module for system-specific parameters and functions

# Get the directory of the executable
exe_dir = os.path.dirname(sys.argv[0])  # Fetching the directory path of the current executable

# Construct the path to activities.txt relative to the executable directory
activities_file = os.path.join(exe_dir, "activities.txt")  # Creating the path to activities.txt relative to exe_dir

# Function to save the activity details to a text file
def save_activity(date, name, length, completed, parent):
    """
    Saves the details of an activity to the activities.txt file.
    
    Parameters:
    - date: Date of the activity.
    - name: Name of the activity.
    - length: Length of the activity in minutes.
    - completed: Boolean indicating if the activity is completed.
    - parent: Parent window to display message box.

    Returns:
    - None
    """
    status = "n" if not completed else "c"  # Determine status based on completion
    with open(activities_file, "a") as file:
        file.write(f"{date},{name},{length},{status}\n")  # Write activity details to file
    parent.lift()
    parent.attributes('-topmost', 1)
    messagebox.showinfo("Saved", "Activity saved successfully!", parent=parent)  # Show confirmation message
    parent.attributes('-topmost', 0)

# Function to read activities from the text file
def read_activities():
    """
    Reads activities stored in activities.txt file and returns them as a list of tuples.
    
    Returns:
    - List of tuples representing activities (date, name, length, status)
    """
    activities = []
    if os.path.exists(activities_file):
        with open(activities_file, "r") as file:
            for line in file:
                date, name, length, status = line.strip().split(',')
                activities.append((date, name, length, status))  # Append activity details to list
    return activities

# Function to update and save activity details in the text file
def update_activity(date, name, length, status):
    """
    Updates the activity details in activities.txt file with new provided details.
    
    Parameters:
    - date: Date of the activity to be updated.
    - name: Name of the activity to be updated.
    - length: New length of the activity in minutes.
    - status: Updated status of the activity ('c' for completed, 'n' for not completed).

    Returns:
    - None
    """
    updated_activities = []
    activities = read_activities()

    # Update the selected activity in the list
    for activity in activities:
        if (activity[0], activity[1]) == (date, name):
            updated_activities.append((date, name, length, status))  # Update activity if found
        else:
            updated_activities.append(activity)

    # Write the updated activities back to the file
    with open(activities_file, "w") as file:
        for date, name, length, status in updated_activities:
            file.write(f"{date},{name},{length},{status}\n")  # Rewrite updated activities to file

# Function to open the Plan page in a new window
def open_plan_page():
    """
    Opens the Plan page with a calendar widget and input fields for activity details.
    
    Returns:
    - None
    """
    plan_window = ctk.CTkToplevel()  # Create a new top-level window for Plan page
    plan_window.title("Plan Page")  # Set window title
    plan_window.geometry("1000x800")  # Set window size

    # Frame for the input fields on the left side
    input_frame = ctk.CTkFrame(plan_window)
    input_frame.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")

    # Frame for the calendar on the right side
    calendar_frame = ctk.CTkFrame(plan_window)
    calendar_frame.grid(row=0, column=1, padx=40, pady=40, sticky="nsew")

    plan_window.grid_columnconfigure(0, weight=1)
    plan_window.grid_columnconfigure(1, weight=2)
    plan_window.grid_rowconfigure(0, weight=1)

    def save_details():
        """
        Retrieves input values and saves activity details when 'Save Activity' button is clicked.
        
        Returns:
        - None
        """
        date = cal.get_date()
        name = name_var.get()
        length = length_var.get()
        if not name or not length:
            messagebox.showwarning("Input Error", "Please enter both name and length of the activity.", parent=plan_window)
        else:
            save_activity(date, name, length, False, plan_window)  # Always set initial status as False (not completed)

    # Creating and packing the calendar widget
    cal = Calendar(calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(expand=True, fill="both", padx=40, pady=40)

    name_var = StringVar()
    length_var = IntVar()

    # Creating and packing the input fields and labels
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
    """
    Opens the Track page with options to select and update activity details.
    
    Returns:
    - None
    """
    track_window = ctk.CTkToplevel()  # Create a new top-level window for Track page
    track_window.title("Track Page")  # Set window title
    track_window.geometry("800x600")  # Set window size
    
    track_window.lift()
    track_window.attributes('-topmost', True)
    track_window.focus_force()

    activities = read_activities()
    activity_names = [f"{index} - {date} - {name}" for index, (date, name, length, status) in enumerate(activities)]

    actual_time_var = IntVar()
    completed_var = IntVar()

    def update_selected_activity():
        """
        Updates the selected activity with new time spent and completion status.
        
        Returns:
        - None
        """
        selected_index = activity_combobox.get()
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

    # Label and Dropdown for selecting activity
    activity_label = ctk.CTkLabel(track_window, text="Select Activity", font=("Helvetica", 16))
    activity_label.pack(pady=20)

    activity_combobox = ctk.CTkOptionMenu(track_window, values=activity_names, font=("Helvetica", 16))
    activity_combobox.pack(pady=10)

    # Entry for actual time spent
    actual_time_label = ctk.CTkLabel(track_window, text=f"Actual Time Spent on Selected Activity (minutes)", font=("Helvetica", 16))
    actual_time_label.pack(pady=5)
    actual_time_entry = ctk.CTkEntry(track_window, textvariable=actual_time_var, font=("Helvetica", 16))
    actual_time_entry.pack(pady=5)

    # Checkbox for completion status
    completed_checkbox = ctk.CTkSwitch(track_window, text="Completed", variable=completed_var, font=("Helvetica", 16))
    completed_checkbox.pack(pady=10)

    # Button to update activity
    update_button = ctk.CTkButton(track_window, text="Update Activity", command=update_selected_activity, font=("Helvetica", 16))
    update_button.pack(pady=20)

# Function to open the Reports page in a new window
def open_reports_page():
    """
    Opens the Reports page with basic information.
    
    Returns:
    - None
    """
    reports_window = ctk.CTkToplevel()  # Create a new top-level window for Reports page
    reports_window.title("Reports Page")  # Set window title
    reports_window.geometry("600x400")  #
