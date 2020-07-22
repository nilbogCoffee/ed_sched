import csv
from classes import Teacher, Certification, LabTime, Stage1And2Student, Stage3Student

def create_student_certifications(certification): #There are semi-colons in the csv from forms
    """
    Create certification objects from a list of certifications from a student using their certified grades and subjects
    """
    return [create_student_certification(cert) for cert in certification.split(', ')]


def create_student_certification(certification):
    """
    Creates one certification object from subject and grade
    """
    def get_subject():
        return certification[certification.rfind(':') + 2:]

    def get_grades():
        grades = certification[certification.find('(') + 8 : certification.find(')')]
        if grades[0] == 'K':
            grades[0] = '0'
        elif grades[0] == 'P':
            grades = grades.replace('PK', '-1')
        grades = grades.rsplit('-', 1)
        return list(range(int(grades[0]), int(grades[1]) + 1))
    
    return Certification(subject=get_subject(), grades=get_grades()) if certification != 'Other' else 'Other'


def create_times(times):
    """
    Create lab time objects based on the day and time of the list of labs from a student
    """
    return [create_time(time) for time in times.split(', ') if times and 'None' not in time]


def create_time(time):
    """
    Create a single LabTime object based on the day and time of the lab
    """
    end_index = time.rfind(' ')
    def get_days():
        return time[time.find(':')+2 : end_index].split('/')

    def get_time():
        return time[end_index+1:]
    
    return LabTime(days=get_days(), time=get_time())


def make_students(file_name):
    """
    Create all student objects from the file
    """
    stage_1_and_2_students = []
    stage_3_students = []
    students = csv.DictReader(open(file_name, encoding='utf-8-sig'))   # Need encoding field to delete the Byte Order Mark (BOM)
    for student in students:
        email = student['Email Address']
        first_name = student['First Name']
        last_name = student['Last Name']
        stage = student['Stage']
        certification = student['Certification(s)']
        transportation = student['Transportation']
        transport_others = student['Transport Others']
        past_schools = [student['School 1'].lower(), student['School 2'].lower(), student['School 3'].lower(), student['School 4'].lower()]

        certification = create_student_certifications(certification)

        if stage == 'Stage 1 & 2':
            all_lab_times = student['Preferred Time'] + ', ' + student['Alternate Time']
            lab_times = create_times(all_lab_times)

            new_student = Stage1And2Student(email=email,
                                            name=first_name + ' ' + last_name,
                                            certifications=certification,
                                            transportation=transportation == 'Yes',
                                            transport_others=transport_others == 'Yes',
                                            preferred_lab_time=lab_times[0],
                                            alt_lab_times = lab_times[1:],
                                            past_schools=past_schools)
            stage_1_and_2_students.append(new_student)

        elif stage == 'Stage 3':
            time_260 = student['260 Time']
            time_360 = student['360-366 Time']
            time_368 = student['368 Time'] 
            time_3582 = student['358.2 Time']
            lab_times = create_times(time_260) + create_times(time_360) + create_times(time_368) + create_times(time_3582)
            
            new_student = Stage3Student(email=email,
                                        name=first_name + ' ' + last_name,
                                        certifications=certification,
                                        transportation=transportation == 'Yes',
                                        transport_others=transport_others == 'Yes',
                                        lab_times=lab_times,
                                        past_schools=past_schools)

            stage_3_students.append(new_student)

    return stage_1_and_2_students, stage_3_students


def make_teachers(file_name):
    """
    Create all teacher objects from the Tidy_Ed_Data_Students.csv file
    """
    teacher_list = []
    teachers = csv.DictReader(open(file_name, encoding='utf-8-sig'))   # Need encoding field to delete the Byte Order Mark (BOM)
    fieldnames = teachers.fieldnames    # Gets the fieldnames from the csv file so we do not have to hardcode values
    for teacher in teachers:
        email = teacher['Email address']
        name = teacher['Teacher\'s Full Name']
        school = teacher['School Name']
        certification = teacher['Subject']
        grade = teacher['Grade']
        district = teacher['District/Entity'] # Eventually
        other_district = teacher.get('If Other, please indicate district')
        stage_3_times = teacher['Stage 3 Lab']
        stage_1_and_2_times = teacher['Stage 1 & 2 Lab']

        new_teacher = Teacher(email=email,
                              name=name,
                              school=school, #district if district != 'Other' else other_district
                              certification=certification,
                              grade=grade, # Formatted differently check
                              stage2_times=create_times(stage_1_and_2_times),
                              stage3_times=create_times(stage_3_times))

        teacher_list.append(new_teacher)
    
    return teacher_list


def check_certification(student, teacher):
    """
    Check if teacher grade and subject are in one of the student's certifications
    """
    # student_certifications = student.get_certifications()
    # teacher_subject = teacher.get_certification()
    # teacher_grade = teacher.get_grade()

    # for cert in student_certifications:
    #     if cert.get_subject() == teacher_subject and teacher.get_grade() in cert.get_grades():
    #         return True

    # return False
    return any([cert.get_subject() == teacher.get_certification() and 
                teacher.get_grade() in cert.get_grades() 
                for cert in student.get_certifications()])
    # Use filter to return time if needed
    # return list(filter(lambda cert: cert.get_subject() == teacher.get_certification() and teacher.get_grade() in cert.get_grades(), 
    #                    student.get_certifications()))


def check_stage_1_and_2_preferred(student, teacher):
    """
    Only used for stage 1 and 2 students for preferred times.
    This function will be used after stage 3 students are handled
    """
    return student.get_preferred_time() in teacher.get_stage2_times()
    # return student.get_preferred_time() if student.get_preferred_time() in teacher.get_stage2_times() else ''

def check_stage_1_and_2_alternate(student, teacher):
    """
    Only used for stage 1 and 2 students for there alternate times
    This function is used after preferred times are handled for all students
    """
    # student_times = student.get_alternate_times()
    # teacher_times = teacher.get_stage2_times()
    # for time in student_times:
    #     if time in teacher_times:
    #         return True

    # return False
    return any([time in teacher.get_stage2_times() for time in student.get_alternate_times()])
    # return list(filter(lambda ele: ele in teacher.get_stage2_times(), student.get_alternate_times()))
    

def check_stage_3_times(student, teacher):
    """
    Only used for stage 3 students for there lab times
    This function is used first before stage 1 & 2 students are considered
    """
    # student_times = student.get_lab_times()
    # teacher_times = teacher.get_stage3_times()
    # for time in student_times:
    #     if time in teacher_times:
    #         return True

    # return False
    return any([time in teacher.get_stage3_times() for time in student.get_lab_times()])
    # Use filter to return time if needed
    # return list(filter(lambda time: time in teacher.get_stage3_times(), student.get_lab_times()))

def check_school(student, teacher):
    """Check that the teacher's school is not in the students list of previous schools"""
    return teacher.get_school() in student.get_schools()
    # return teacher.get_school() if teacher.get_school() not in student.get_schools() else ''


def check_transport(student, teacher):
    """Check that the student can drive or walk"""
    return student.get_transportation()


def print_sched(teachers):
    """Print the schedule results"""
    for teacher in teachers:
        student = teacher.get_student()
        if student and student.get_other_drivers():
            print(f"{student.get_name()} will join {teacher.get_name()}. {student.get_name()} should get a ride from:", 
                   ', '.join([driver.get_name() for driver in student.get_other_drivers()]))
        elif student:
            print(f"{student.get_name()} will join {teacher.get_name()}")
        # else:
        #     print(f"{teacher.get_name()} has no student.")


def perform_checks(student, teacher, alternate_time):
    """
    Perform all checks between student and teacher to see if they are compatible
    Returns a tuple of whether the match is found and whether the student can commute
    """
    # Start here next time
    subject = check_subject(student, teacher)
    grade = check_grade(student, teacher)
    school = check_school(student, teacher)
    teacher_is_taken = teacher.get_match_found()
    student_can_commute = check_transport(student, teacher)
    if isinstance(student, Stage3Student):
        pass
    elif isinstance(student, Stage1And2Student) and alternate_time:
        pass
    else:
        pass
    availability = check_availability(student, teacher) # Change based on which instance is passed in
    

    return subject and grade and availability and not school and not teacher_is_taken, student_can_commute
    # Maybe return actual values

def match_found(student, teacher):
    """Match found between student and teacher. Sets the teacher's student. Overwrites the student's availability"""
    teacher.set_match_found(True)
    student.set_match_found(True)
    teacher.set_student(student)
    student.set_availability(teacher.get_availability())  # Overwrite the student's availability to the teacher's availability


def matchmaker(students, teachers, alternate_time=False):
    """
    Determines which students are matches with each teacher by each student object attribute
    This is the main function that this program is centered around
    """
    students_need_ride = []
    for student in students:
        for teacher in teachers:
            student_matches_teacher, student_can_commute = perform_checks(student, teacher, alternate_time)
            
            if student_matches_teacher:
                match_found(student, teacher)

                if not student_can_commute:
                    students_need_ride.append(student)
    
    assign_drivers(students_need_ride, students)
    print_sched(teachers)


def assign_drivers(students_need_ride, all_students):
    """Students that need a ride are given a list of students that are available for car pool"""
    for student in students_need_ride:
       for driver in all_students:
           if driver.get_availability() == student.get_availability() and driver.get_can_car_pool():
               student.add_driver(driver)


def write_schedule(teachers):
    """Write results to csv file"""
    with open("sched.csv", "w") as schedule:
        writer = csv.DictWriter(schedule, fieldnames=["Student", "Teacher", "School", "Lab"])
        writer.writeheader()

        for teacher in teachers:
            if teacher.get_match_found():
                writer.writerow({"Student": teacher.get_student().get_name(), 
                                 "Teacher": teacher.get_name(), 
                                 "School": teacher.get_school(),
                                 "Lab": teacher.get_availability()})


def write_extra_students(students):
    """Write the students that have no assigned field experience to a csv file"""
    with open("unmatched_students.csv", "w") as schedule:
        writer = csv.DictWriter(schedule, fieldnames=["Student","Lab", "Can Drive"])
        writer.writeheader()

        for student in students:
            if not student.get_match_found():
                writer.writerow({"Student": student.get_name(), 
                                 "Lab": ','.join(student.get_availability()), 
                                 "Can Drive": 'Yes' if student.get_can_drive() else 'No'})


def main():
    stage_1_and_2_students, stage_3_students = make_students("sheetsFile.csv")
    teachers = make_teachers("teachers.csv")
    for student in stage_1_and_2_students:
        print()
        print(student)
    for student in stage_3_students:
        print()
        print(student)

    # print()
    for teacher in teachers:
        print(teacher)

    # print()
    # matchmaker(stage_3_students, teachers)
    # matchmaker(stage_1_and_2_students, teachers)
    # matchmaker(stage_1_and_2_students, teachers, alternate_time=True)

    # write_schedule(teachers)
    # write_extra_students(students)


if __name__ == '__main__':
    main()


"""
TODO: 
1. Write bash script to actually run the program so that a user can execute program on double click of the bash script
2. Make GUI visually appealing and check for user error
"""