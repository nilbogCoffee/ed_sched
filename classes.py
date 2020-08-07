class Student:
    """
    Student parent class
    """
    def __init__(self, email: str, name: str, certifications: list, transportation: bool, transport_others: bool, past_schools: list,
                 transportation_comments: str, lab_comments: str):
        self.email = email
        self.name = name
        self.certifications = certifications
        self.transportation = transportation
        self.transport_others = transport_others
        self.past_schools = past_schools
        self.match_found = False
        self.other_drivers = []
        self.transportation_comments = transportation_comments
        self.lab_comments = lab_comments

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_certifications(self):
        return self.certifications

    def set_certifications(self, certifications):
        self.certifications = certifications

    def get_transportation(self):
        return self.transportation

    def set_transportation(self, transportation):
        self.transportation = transportation

    def get_transport_others(self):
        return self.transport_others

    def set_transport_others(self, transport_others):
        self.transport_others = transport_others

    def get_transportation_comments(self):
        return self.transportation_comments

    def set_transportation_comments(self, comment):
        self.transportation = comment

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

    def get_lab_times(self):
        return self.lab_times

    def set_lab_times(self, lab_times):
        self.lab_times = lab_times

    def get_lab_comments(self):
        return self.lab_comments

    def set_lab_comments(self, comment):
        self.lab_comments = comment

    def __str__(self):
        certifications = ', '.join(map(lambda cert: cert.__str__(), self.get_certifications()))
        return (f'Email: {self.get_email()}\n'
                f'Name: {self.get_name()}\n'
                f'Certification: {certifications}\n'
                f'Transportation: {self.get_transportation()}\n'
                f'Transport Others: {self.get_transport_others()}\n'
                f'Past Schools: {self.get_past_schools()}')


class Stage1And2Student(Student):
    """
    Subclass of Student class. Only difference is preferred lab time and alternate lab times
    """
    def __init__(self, email: str, name: str, certifications: list, transportation: bool, transport_others: bool, 
                 preferred_lab_time: str, alt_lab_times: list, past_schools: list, transportation_comments: str, lab_comments: str):
        super().__init__(email, name, certifications, transportation, transport_others, past_schools, transportation_comments, lab_comments)
        self.preferred_lab_time = preferred_lab_time
        self.alt_lab_times = alt_lab_times
        self.lab_times = [self.preferred_lab_time] + self.alt_lab_times

    def get_preferred_lab_time(self):
        return self.preferred_lab_time

    def set_preferred_lab_time(self, time):
        self.preferred_lab_time = time

    def get_alt_lab_times(self):
        return self.alt_lab_times

    def set_alt_lab_times(self, times):
        self.alt_lab_times = times

    def __str__(self):
        alt_lab_times = ', '.join(map(str, self.get_alt_lab_times()))
        return super().__str__() + (f'\nPreferred Lab Time: {self.get_preferred_lab_time()}'
                                    f'\nAlternate Lab Times: {alt_lab_times}')


class Stage3Student(Student):
    """
    Subclass of Student class for Stage 3 students. Only difference is lab times
    """
    def __init__(self, email: str, name: str, certifications: list, transportation: bool, transport_others: bool, 
                 past_schools: list, lab_times: list, transportation_comments: str, lab_comments: str):
        super().__init__(email, name, certifications, transportation, transport_others, past_schools, transportation_comments, lab_comments)
        self.lab_times = lab_times

    def __str__(self):
        lab_times = ', '.join(map(str, self.get_lab_times()))
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
        grades = ', '.join(map(str, self.get_grades()))
        return f'[Subject: {self.get_subject()}, Grades: {grades}]'

           
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

    def __eq__(self, other):
        return self.days == other.days and self.time == other.time if isinstance(other, LabTime) else False

    def __str__(self):
        days = ', '.join(self.get_days())
        return  f'[Days: {days}, Time: {self.get_time()}]'


class Teacher:
    """
    Teacher class
    """

    def __init__(self, email: str, name: str, school: str, certification: str, stage2_times: list, stage3_times: list):
        self.email = email
        self.name = name
        self.certification = certification
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

    def get_certification(self):
        return self.certification

    def set_certification(self, certification):
        self.certification = certification

    def get_stage2_times(self):
        return self.stage2_times

    def set_stage2_times(self, times):
        self.stage2_times = times

    def get_stage3_times(self):
        return self.stage3_times

    def set_stage3_times(self, times):
        self.stage3_times = times

    def get_all_lab_times(self):
        return self.get_stage2_times() + self.get_stage3_times()

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
        stage2times = ', '.join(map(str, self.get_stage2_times()))
        stage3times = ', '.join(map(str, self.get_stage3_times()))
        return (f'Email: {self.get_email()}\n'
                f'Name: {self.get_name()}\n'
                f'Certification: {self.get_certification()}\n'
                f'Stage2 Times: {stage2times}\n'
                f'Stage3 Times: {stage3times}\n'
                f'School: {self.get_school()}\n'
                f'Student: {self.get_student()}\n')
