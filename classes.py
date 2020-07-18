class Student:
    """
    Student parent class
    """

    def __init__(self, email: str, name: str, certifications: list, transportation: bool, transport_others: bool, past_schools: list):
        self.email = email
        self.name = name
        self.certifications = certifications
        self.transportation = transportation
        self.transport_others = transport_others
        self.past_schools = past_schools
        self.match_found = False
        self.other_drivers = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_certifications(self):
        return self.certifications

    def set_certifications(self, certifications):
        self.certifications = certifications

    def get_trasportaion(self):
        return self.transportation

    def set_transportation(self, transportation):
        self.transportation = transportation

    def get_transport_others(self):
        return self.transport_others

    def set_transport_others(self, transport_others):
        self.transport_others = transport_others

    def get_past_schools(self):
        return self.past_schools

    def set_past_schools(self, past_schools):
        self.past_schools = past_schools

    def get_match_found(self):
        return self.match_found
    
    def set_match_found(self, match_found):
        self.match_found = match_found
        
    def get_other_drivers(self):
        return self.other_drivers

    def set_other_drivers(self, other_drivers):
        self.other_drivers = other_drivers
    
    def add_driver(self, other_driver):
        self.other_drivers.append(other_driver)

    def get_email(self):
        return self.email
    
    def set_email(self, email):
        self.email = email

    def __str__(self):
        certifications = ', '.join(map(lambda cert: cert.__str__(), self.get_certifications()))
        return (f'Email: {self.get_email()}\n'
                f'Name: {self.get_name()}\n'
                f'Certification: {certifications}\n'
                f'Transportation: {self.get_trasportaion()}\n'
                f'Transport Others: {self.get_transport_others()}\n'
                f'Past Schools: {self.get_past_schools()}')


class Stage1And2Student(Student):
    """
    Subclass of Student class. Only difference is preferred lab time and alternate lab times
    """
    def __init__(self, email: str, name: str, certifications: list, transportation: bool, transport_others: bool, 
                 preferred_lab_time: str, alt_lab_times: list, past_schools: list):
        super().__init__(email, name, certifications, transportation, transport_others, past_schools)
        self.preferred_lab_time = preferred_lab_time
        self.alt_lab_times = alt_lab_times

    def get_preferred_lab_time(self):
        return self.preferred_lab_time

    def set_preferred_lab_time(self, time):
        self.preferred_lab_time = time

    def get_alt_lab_times(self):
        return self.alt_lab_times

    def set_alt_lab_times(self, times):
        self.alt_lab_times = times

    def __str__(self):
        alt_lab_times = ', '.join(map(lambda lab_time: lab_time.__str__(), self.get_alt_lab_times()))
        return super().__str__() + (f'\nPreferred Lab Time: {self.get_preferred_lab_time()}'
                                    f'\nAlternate Lab Times: {alt_lab_times}')


class Stage3Student(Student):
    """
    Subclass of Student class for Stage 3 students. Only difference is lab times
    """
    def __init__(self, email: str, name: str, certifications: list, transportation: bool, transport_others: bool, 
                 past_schools: list, lab_times: list):
        super().__init__(email, name, certifications, transportation, transport_others, past_schools)
        self.lab_times = lab_times

    def get_lab_times(self):
        return self.lab_times

    def set_lab_times(self, times):
        self.lab_times = times

    def __str__(self):
        lab_times = ', '.join(map(lambda time: time.__str__(), self.get_lab_times()))
        return super().__str__() + f'\nLab Times: {lab_times}'


class Certification:
    """
    Class for the subject and grades of a certification
    """
    def __init__(self, subject, grades):
        self.subject = subject
        self.grades = grades

    def get_subject(self):
        return self.subject

    def set_subject(self, subject):
        self.subject = subject

    def get_grades(self):
        return self.grades

    def set_grades(self, grades):
        self.grades = grades 

    def __str__(self):
        return (f'Subject: {self.get_subject()}\n'
                f'Grades: {self.get_grades()}')

           
class LabTime:
    """
    Class for days and times of labs
    """
    def __init__(self, days, time):
        self.days = days
        self.time = time

    def get_days(self):
        return self.days

    def set_days(self, days):
        self.days = days

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time

    def __str__(self):
        return (f'Days: {self.get_days()}\n'
                f'Time: {self.get_time()}')


class Teacher:
    """
    Teacher parent class
    """

    def __init__(self, email: str, name: str, school: str, certifications: str, grade: str, stage2_times: list, stage3_times: list):
        self.email = email
        self.name = name
        self.certifications = certifications
        self.grade = grade
        self.school = school
        self.stage2_times = stage2_times
        self.stage3_times = stage3_times
        self.match_found = False
        self.student = None

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_certifications(self):
        return self.certifications

    def set_certifications(self, certifications):
        self.certification = certifications

    def get_grade(self):
        return self.grade

    def set_grade(self, grade):
        self.grade = grade

    def get_stage2_times(self):
        return self.stage2_times

    def set_stage2_times(self, times):
        self.stage2_times = times

    def get_stage3_times(self):
        return self.stage3_times

    def set_stage3_times(self, times):
        self.stage3_times = times

    def get_school(self):
        return self.school

    def set_school(self, school):
        self.school = school

    def get_match_found(self):
        return self.match_found

    def set_match_found(self, match_found):
        self.match_found = match_found
    
    def get_student(self):
        return self.student
    
    def set_student(self, student):
        self.student = student
    
    def __str__(self):
        return str({'email': self.get_email(),
                    'name': self.get_name(),
                    'certification': self.get_certification(),
                    'grade': self.get_grade(),
                    'stage2 times': self.get_stage2_times(),
                    'stage3 times': self.get_stage3_times(),
                    'school': self.get_school(),
                    'student': self.get_student()})
