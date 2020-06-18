class Student:

    def __init__(self, name, subject, grades, availability, can_drive, experience):
        self.name = name
        self.subject = subject
        self.grades = grades
        self.availability = availability
        self.can_drive = can_drive
        self.experience = experience

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_subject(self):
        return self.subject

    def set_subject(self, subject):
        self.subject = subject

    def get_grades(self):
        return self.grades

    def set_grades(self, grades):
        self.grades = grades

    def get_availability(self):
        return self.availability

    def set_availability(self, availability):
        self.availability = availability

    def get_can_drive(self):
        return self.can_drive

    def set_can_drive(self, can_drive):
        self.can_drive = can_drive

    def get_experience(self):
        return self.experience

    def set_experience(self, experience):
        self.experience = experience

    def __str__(self):
        return self.get_name() + self.get_subject() + str(self.get_grades()) + str(self.get_availability()) + self.get_can_drive() + str(self.get_experience())


class Teacher:

    def __init__(self, name, subject, grade, school, availability, can_walk):
        self.name = name
        self.subject = subject
        self.grade = grade
        self.school = school
        self.availability = availability
        self.can_walk = can_walk

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_subject(self):
        return self.subject

    def set_subject(self, subject):
        self.subject = subject

    def get_grade(self):
        return self.grade

    def set_grade(self, grade):
        self.grade = grade

    def get_availability(self):
        return self.availability

    def set_availability(self, availability):
        self.availability = availability

    def get_school(self):
        return self.school

    def set_school(self, school):
        self.school = school

    def get_can_walk(self):
        return self.can_walk

    def set_can_walk(self, can_walk):
        self.can_walk = can_walk
    
    def __str__(self):
        return self.get_name() + self.get_subject() + self.get_grade() + self.get_availability() + self.get_school() + self.get_can_walk()

