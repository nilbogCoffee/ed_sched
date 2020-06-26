import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

class run_GUI:
    """
    This class is used to run the GUI for this program.
    First, it asks for 2 files that the user can choose from their Finder Menu after hitting the Browse button
    It validates to make sure that only two files are being used. The user may enter them one at a time as well.
    Then, it lists the filenames without their full paths that the user has provided.
    Lastly, it exposes the run button to run the scheduler
    """

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Field Experience Scheduler")
        self.filenames = []
        self.listbox = tk.Listbox()

    def choose_files(self):
        """Uses Tkinter's filedialog library to ask for multiple files from the user while exposing their Finder Menu"""
        print('asking for files')
        filenames = filedialog.askopenfilenames()
        self.display_files(filenames)
        
    def display_files(self, filenames):
        """Displays the filenames without their full paths and validates that there are at most two"""
        # for count, filename in enumerate(filenames, 0):
        #     relative_filename = filename[filename.rfind('/') + 1:]
        #     self.listbox.insert(count, f"File {count + 1}: {relative_filename}")

        # If there are two files in the listbox already
        if self.listbox.size() == 2:
            return

        # If there is only one file in the listbox already
        if self.listbox.size() == 1:
            self.add_file(filenames[0])
            self.listbox.insert(1, "File 2: " + self.get_filename(filenames[0]))

        # If the listbox is empty
        else:
            self.listbox.insert(0, "File 1: " + self.get_filename(filenames[0]))
            self.add_file(filenames[0])
            if len(filenames) == 2:
                self.listbox.insert(1, "File 2: " + self.get_filename(filenames[1]))
                self.add_file(filenames[1])

        self.listbox.pack()

    def get_filename(self, filename):
        """Parses the file's full path for just the name of the file"""
        return filename[filename.rfind('/') + 1:]

    def add_file(self, filename):
        """Adds a file to the list of files that are being used by the scheduler"""
        self.filenames.append(filename)

    def create_first_screen(self):
        """Creates the first screen with the heading and button and begins the event handler"""
        label = tk.Label(master=self.window, text="Choose both the student and teacher .csv files you wish to use for scheduling:").pack()
        button = ttk.Button(master=self.window, text="Browse Files", command=self.choose_files).pack()
        self.window.mainloop()

    def get_filenames(self):
        return self.filenames


    # def run(self):

# Using this for debugging at the moment
run = run_GUI()
run.create_first_screen()

