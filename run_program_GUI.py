import os
import subprocess
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from ed_code2 import make_students, make_teachers, matchmaker, write_schedule, write_unmatched_students, assign_drivers, make_workbook

class run_GUI:
    """
    This class is used to run the GUI for this program.
    First, it asks for 2 files that the user can choose from their Finder Menu after hitting the Browse buttons
    Then, it lists the filenames without their full paths that the user has provided.
    Lastly, it exposes the run button to run the scheduler
    """

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Field Experience Scheduler")
        self.filenames = {}
        self.downloads_folder = os.path.expanduser('~')+'/Downloads'
        self.confirmation_teacher_label = None
        self.confirmation_student_label = None
        self.create_schedule = None
        self.open_file_label = None
        self.error_label = None


    def check_run_button(self):
        if self.error_label:
            self.error_label.destroy()
            self.error_label = None
        if len(self.filenames) == 2 and not self.create_schedule:
            self.expose_run_button()


    def display_student_file(self, filename):
        """Add the file to the filenames dictionary and retrieve the file's name without the full path to display it"""
        self.add_file(filename, 'Student')
        filename = self.parse_filename(filename)
        if self.confirmation_student_label:
            self.confirmation_student_label.configure(text=f"Student file: {filename}")
        else:
            self.confirmation_student_label = tk.Label(master=self.window, font=('calibri', 18), text=f"Student file: {filename}")
            self.confirmation_student_label.pack()
        self.check_run_button()

    
    def display_teacher_file(self, filename):
        self.add_file(filename, 'Teacher')
        filename = self.parse_filename(filename)
        if self.confirmation_teacher_label:
            self.confirmation_teacher_label.configure(text=f"Teacher file: {filename}")
        else:
            self.confirmation_teacher_label = tk.Label(master=self.window, font=('calibri', 18), text=f"Teacher file: {filename}")
            self.confirmation_teacher_label.pack()
        self.check_run_button()


    def choose_student_file(self):
        """Retrieve the full path for the student .csv file from the Finder Menu"""
        filename = filedialog.askopenfilename(initialdir=os.getenv('HOME', '/'), 
                                              title="Select A Student .csv File", 
                                              filetypes=(("csv files","*.csv"),))
        if not filename:
            return # Error message
        self.display_student_file(filename)


    def choose_teacher_file(self):
        """Retrieve the full path for the teacher .csv file from the Finder Menu"""
        filename = filedialog.askopenfilename(initialdir=os.getenv('HOME', '/'), 
                                              title="Select A Teacher .csv File", 
                                              filetypes=(("csv files","*.csv"),))
        if not filename:
            return # Error message
        self.display_teacher_file(filename)


    def parse_filename(self, filename):
        """Parses the file's full path for just the name of the file"""
        return filename[filename.rfind('/') + 1:]


    def add_file(self, filename, type_of_file):
        """Adds a file to the list of files that are being used by the scheduler"""
        self.filenames[type_of_file] = filename


    def create_widgets(self):
        """Creates the first screen with the heading and button and begins the event handler"""
        small_label_font = ("calibri", 15, "underline")
        label = tk.Label(master=self.window, font=("calibri", "20", "bold"), text="Choose both the student and teacher .csv files you wish to use for scheduling:").pack()

        student_label = tk.Label(master=self.window, font=small_label_font, text="Choose the student .csv file:").pack()
        student_button = ttk.Button(master=self.window, text="Browse Files", command=self.choose_student_file).pack()

        teacher_label = tk.Label(master=self.window, font=small_label_font, text="Choose the teacher .csv file:").pack()
        teacher_button = ttk.Button(master=self.window, text="Browse Files", command=self.choose_teacher_file).pack()
        
        self.window.mainloop()


    def get_filenames(self):
        return self.filenames


    def expose_run_button(self):
        """Creates the run button and links it to the run function which begins the scheduling from within the ed_code2.py file"""
        style = ttk.Style()
        style.configure('K.TButton', foreground="green", font="helvetica 24 bold")
        self.create_schedule = ttk.Button(master=self.window, text="Create Schedule", style="K.TButton", command=self.run)
        self.create_schedule.pack()


    def display_open_message(self):
        self.open_file_label = tk.Label(master=self.window, text="Open csv files?")
        self.open_file_label.pack()

        top = tk.Frame(self.window)
        bottom = tk.Frame(self.window)
        top.pack(side=tk.TOP)
        bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        yes_button = ttk.Button(master=self.window, text="Open in Excel", command=lambda: self.open_files('Microsoft Excel'))
        num_button = ttk.Button(master=self.window, text="Open in Numbers", command=lambda: self.open_files('Numbers'))
        no_button = ttk.Button(master=self.window, text="No", command=lambda: self.window.destroy())

        yes_button.pack(in_=top, side=tk.LEFT)
        num_button.pack(in_=top, side=tk.LEFT)
        no_button.pack(in_=top, side=tk.LEFT)


    def open_files(self, app):
        try:
            # subprocess.run(['open', self.downloads_folder+'/unmatched_students.csv', self.downloads_folder+'/sched.csv', '-a', 'Microsoft Excel'], check=True)
            subprocess.run(['open', self.downloads_folder + '/Schedule.xlsx', '-a', app], check=True)
        except:
            subprocess.run(['open', self.downloads_folder + '/Schedule.xlsx'], check=True)

        self.window.destroy()


    def run(self):
        try:
            stage_1_and_2_students, stage_3_students = make_students(self.get_filenames()['Student'])
            teachers = make_teachers(self.get_filenames()['Teacher'])
            if self.error_label:
                self.error_label.destroy()
        except:
            if not self.error_label:
                self.error_label = tk.Label(master=self.window,
                                            font=("calibri", 25, "bold underline"),
                                            fg="red",
                                            text="Cannot read files! Make sure to download csv files directly from the generated Google Sheet.")
                self.error_label.pack()
            return

        stage_3_leftover, stage_3_need_ride = matchmaker(stage_3_students, teachers) 
        matchmaker(stage_1_and_2_students, teachers)
        stage_1_and_2_leftover, stage_1_and_2_need_ride = matchmaker(stage_1_and_2_students, teachers, alternate_time=True)

        assign_drivers(stage_3_need_ride + stage_1_and_2_need_ride, stage_1_and_2_students + stage_3_students)
        workbook = make_workbook()
        write_schedule(teachers, workbook)
        write_unmatched_students(stage_3_leftover + stage_1_and_2_leftover, workbook)
        workbook.save(self.downloads_folder + '/Schedule.xlsx')

        if not self.open_file_label:
            self.display_open_message()

