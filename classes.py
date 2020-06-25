class Student:
    """
    Student parent class
    """

    def __init__(self, name: str, subject: str, grades: list, availability: list, can_drive: bool, can_car_pool: bool, experience: list, match_found=False):
        self.name = name
        self.subject = subject
        self.grades = grades
        self.availability = availability
        self.can_drive = can_drive
        self.can_car_pool = can_car_pool
        self.experience = experience
        self.match_found = match_found
        self.other_drivers = []

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

    def get_can_car_pool(self):
        return self.can_car_pool

    def set_can_car_pool(self, can_car_pool):
        self.can_car_pool = can_car_pool

    def get_experience(self):
        return self.experience

    def set_experience(self, experience):
        self.experience = experience

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

    def __str__(self):
        return str({'name': self.get_name(),
                'subject': self.get_subject(),
                'grades': self.get_grades(),
                'availability': self.get_availability(),
                'can_drive': self.get_can_drive(),
                'can_car_pool': self.get_can_car_pool(),
                'experience': self.get_experience()})


class Teacher:
    """
    Teacher parent class
    """

    def __init__(self, name: str, subject: str, grade: str, school: str, availability: str, can_walk: bool, match_found=False, student=None):
        self.name = name
        self.subject = subject
        self.grade = grade
        self.school = school
        self.availability = availability
        self.can_walk = can_walk
        self.match_found = match_found
        self.student = student

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

    def get_match_found(self):
        return self.match_found

    def set_match_found(self, match_found):
        self.match_found = match_found
    
    def get_student(self):
        return self.student
    
    def set_student(self, student):
        self.student = student
    
    def __str__(self):
        return str({'name': self.get_name(),
                'subject': self.get_subject(),
                'grade': self.get_grade(),
                'availability': self.get_availability(),
                'school': self.get_school(),
                'can_walk': self.get_can_walk()})
