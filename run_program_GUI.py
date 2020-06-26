import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from ed_code2 import make_students, make_teachers, matchmaker, write_schedule, write_extra_students

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
        self.filenames = {}


    def check_run_button(self):
        if len(self.filenames) == 2:
            self.expose_run_button()


    def display_file(self, filename, type_of_file):
        """Add the file to the filenames dictionary and retrieve the file's name without the full path to display it"""
        self.add_file(filename, type_of_file)
        filename = self.parse_filename(filename)
        tk.Label(master=self.window, text=f"{type_of_file} file: {filename}").pack()
        self.check_run_button()


    def choose_student_file(self):
        """Retrieve the full path for the student .csv file from the Finder Menu"""
        filename = filedialog.askopenfilename()
        self.display_file(filename, 'Student')


    def choose_teacher_file(self):
        """Retrieve the full path for the teacher .csv file from the Finder Menu"""
        filename = filedialog.askopenfilename()
        self.display_file(filename, 'Teacher')


    def parse_filename(self, filename):
        """Parses the file's full path for just the name of the file"""
        return filename[filename.rfind('/') + 1:]


    def add_file(self, filename, type_of_file):
        """Adds a file to the list of files that are being used by the scheduler"""
        self.filenames[type_of_file] = filename


    def create_widgets(self):
        """Creates the first screen with the heading and button and begins the event handler"""
        label = tk.Label(master=self.window, text="Choose both the student and teacher .csv files you wish to use for scheduling:").pack()

        student_label = tk.Label(master=self.window, text="Choose the student .csv file:").pack()
        student_button = ttk.Button(master=self.window, text="Browse Files", command=self.choose_student_file).pack()

        teacher_label = tk.Label(master=self.window, text="Choose the teacher .csv file:").pack()
        teacher_button = ttk.Button(master=self.window, text="Browse Files", command=self.choose_teacher_file).pack()
        
        self.window.mainloop()


    def get_filenames(self):
        return self.filenames


    def expose_run_button(self):
        """Creates the run button and links it to the run function which begins the scheduling from within the ed_code2.py file"""
        run_button = ttk.Button(master=self.window, text="Create Schedule", command=lambda: run(self.get_filenames())).pack()


def run(filenames):
    
    students = make_students(filenames['Student'])
    teachers = make_teachers(filenames['Teacher'])
    
    matchmaker(students, teachers)

    write_schedule(teachers)
    write_extra_students(students)

