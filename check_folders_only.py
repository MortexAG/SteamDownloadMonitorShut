import os
import glob
import time
import tkinter
from tkinter import filedialog, messagebox
import customtkinter
from customtkinter import CTkButton, CENTER, CTkLabel, CTkEntry
import threading


# Path checks
if not os.path.exists("./color_mode.txt"):
    with open("./color_mode.txt", "w") as text:
        text.write("Dark")

if not os.path.exists('./library_location.txt'):
    with open('./library_location.txt', 'w') as text:
        text.write('')

# Define the app
app = customtkinter.CTk()  # Create CTk window
app.title("Check Folders Only")
app.geometry("1000x700")  # Increase the window size to accommodate the larger sidebar

# Sidebar frame with increased width
#sidebar_frame = customtkinter.CTkFrame(app, width=300, corner_radius=0)  # Increase width as needed
#sidebar_frame.pack(side="left", fill="y", expand=False)

# Function to grab the folder path
def grab_folder():
    with open('library_location.txt', 'r') as library:
        return library.read()

# Variables
steam_downloading_folder = grab_folder()

### MAIN APP

# variables
number_of_remainder_folders = 0

folders_list = []

checking = False  # This will be used to control the loop within the thread

# Function to update the folder contents label
def update_folder_contents_label(folders_list):
    folder_contents_str = "\n".join(folders_list)
    folder_contents_label.configure(text=folder_contents_str)


#function when downloading is done

def shutdowm():
    os.system("shutdown -s")

# Function to check the folder, modified for self-scheduling
def start_checking():
    global checking
    if checking:
        with open('library_location.txt', 'r') as library:
            steam_downloading_folder = library.read()

        folders_list = [name for name in os.listdir(steam_downloading_folder) 
                        if os.path.isdir(os.path.join(steam_downloading_folder, name))]

        # Update the GUI with the folder contents
        app.after(0, update_folder_contents_label, folders_list)

        try:
            if len(folders_list) <= int(folder_remainder_entry.get()):
                shutdowm()
        except ValueError:
            # Handle case where entry input is not a valid integer
            #if len(folder_remainder_entry.get()) < 1:
                pass
            #else:    
            #    messagebox.showwarning("Incorrect Input Type", ", Default Value of 0 is Being Used Now, Please Use Integers Only (1,2,3...)")

        # Schedule the next check (e.g., after 300000 milliseconds or 5 minutes)
        app.after(300000, start_checking)  # Adjust the time as needed

# Function to start and stop checking
def toggle_checking():
    steam_downloading_folder = grab_folder()
    if steam_downloading_folder:
        global checking
        #if len(folder_remainder_entry.get()) < 1:
        if not checking:
            checking = True
            start_checking_button.configure(text="Stop Checking")
            start_checking()  # Start the checking process
        else:
            checking = False
            start_checking_button.configure(text="Start Checking")
        #else:
        #    messagebox.showwarning("Incorrect Input Type", "Please Use Integers Only (1,2,3...)")
    else:
        messagebox.showwarning("Downloading Folder Not Chosen", "Please Choose The Downloading Folder First \n\n Commonly Found in \n'C:/Program Files (x86)/Steam/steamapps/downloading'")



# The button now toggles the checking state
start_checking_button = CTkButton(master=app, text="Start Checking", command=toggle_checking)
start_checking_button.place(relx=0.2, rely=0.6, anchor=tkinter.CENTER)  # Adjust the placement as needed

# Entry for user to specify the desired number of remaining folders
#time_interval_entry = CTkEntry(master=app, placeholder_text="Checking Interval Seconds")
#time_interval_entry.place(relx=0.2, rely=0.7, anchor=tkinter.CENTER)

# Entry for user to specify the desired number of remaining folders
folder_remainder_entry = CTkEntry(master=app, placeholder_text="Remaining folders limit")
folder_remainder_entry.place(relx=0.2, rely=0.7, anchor=tkinter.CENTER)

# Label to display "Folder Contents"
folder_contents_label_title = CTkLabel(master=app, text="Folder Contents:")
folder_contents_label_title.place(relx=0.6, rely=0.1, anchor=tkinter.CENTER)

# Label to display the actual folder contents
folder_contents_label = CTkLabel(master=app, text="", fg_color="transparent")
folder_contents_label.place(relx=0.6, rely=0.2, anchor=tkinter.CENTER)


#### SIDEBAR STUFF

# Set the color and theme of the app
with open("color_mode.txt", 'r') as mode:
    color = mode.read()
customtkinter.set_appearance_mode(color)  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green



# Show Library Location
text_label = CTkLabel(app, text="Steam Downloading Location:", fg_color="transparent")
text_label.place(relx=0.2, rely=0.2, anchor=CENTER)

downloading_location_label = CTkLabel(app, text=steam_downloading_folder, fg_color="transparent")
downloading_location_label.place(relx=0.2, rely=0.3, anchor=CENTER)

# Button to choose the Steam downloading folder
def choose_folder():
    folder_selected = filedialog.askdirectory()
    with open("library_location.txt", 'w') as library:
        library.write(folder_selected)
    downloading_location_label.configure(text=folder_selected)

choose_folder_button = CTkButton(master=app, text="Choose The Steam Downloading Folder", command=choose_folder)
choose_folder_button.place(relx=0.2, rely=0.4, anchor=CENTER)

# Button to verify the downloading folder
def check_folder():
    steam_downloading_folder = grab_folder()
    if steam_downloading_folder:
        downloading_location_label.configure(text=steam_downloading_folder)
    else:
        messagebox.showwarning("Downloading Folder Not Chosen", "Please Choose The Downloading Folder First \n\n Commonly Found in \n'C:/Program Files (x86)/Steam/steamapps/downloading'")

check_folder_location_button = CTkButton(master=app, text="Verify Downloading Folder", command=check_folder)
check_folder_location_button.place(relx=0.2, rely=0.5, anchor=CENTER)

# Color mode menu
with open("color_mode.txt", "r") as mode:
    color = mode.read()
    optionmenu_var = customtkinter.StringVar(value=color)  # set initial value

def optionmenu_callback(choice):
    with open("color_mode.txt", "w") as mode:
        mode.write(choice)
    customtkinter.set_appearance_mode(choice)

mode_combobox = customtkinter.CTkOptionMenu(master=app, values=["Dark", "Light", "System"], command=optionmenu_callback, variable=optionmenu_var)
mode_combobox.place(relx=0.2, rely=0.1, anchor=tkinter.CENTER)

app.mainloop()
