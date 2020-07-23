import csv
from classes import Teacher, Certification, LabTime, Stage1And2Student, Stage3Student

def create_student_certifications(certification, other=None): #There are semi-colons in the csv from forms
    """
    Create certification objects from a list of certifications from a student using their certified grades and subjects
    """
    return [create_student_certification(cert, other) for cert in certification.split(', ')]


def create_student_certification(certification, other):
    """
    Creates one certification object from subject and grade
    """
    def get_subject():
        return certification[certification.rfind(':') + 2:]

    def get_grades():
        grades = certification[certification.find('(') + 8 : certification.find(')')]
        if grades[0] == 'P':
            grades = grades.replace('PK', '-1')
        grades = grades.rsplit('-', 1)
        return list(range(int(grades[0]), int(grades[1]) + 1))
    
    return Certification(subject=get_subject(), grades=get_grades()) if certification != 'Other' else other


def create_times(times, other=None):
    """
    Create lab time objects based on the day and time of the list of labs from a student
    """
    return [create_time(time, other) for time in times.split(', ') if times]


def create_time(time, other):
    """
    Create a single LabTime object based on the day and time of the lab
    """
    end_index = time.rfind(' ')
    def get_days():
        return time[time.find(':')+2 : end_index].split('/')

    def get_time():
        return time[end_index+1:]

    
    return LabTime(days=get_days(), time=get_time()) if time != 'Other' else other


def convert_grade(grade):
    if grade[:2] == 'PK':
        grade = [-1]
    elif grade == 'Kindergarten':
        grade = [0]
    elif len(grade) > 1 and grade[:2].isdigit():
        grade = [int(grade[:2])]
    elif grade[0].isdigit():
        grade = [int(grade[0])]
    elif grade.startswith('Special'):
        grade = list(range(-1, 13))
    else:
        grade = [grade]
    
    return grade

def make_students(file_name):
    """
    Create all student objects from the file
    """
    stage_1_and_2_students = []
    stage_3_students = []
    students = csv.DictReader(open(file_name, encoding='utf-8-sig'))   # Need encoding field to delete the Byte Order Mark (BOM)
    for student in students:
        # Just need to check to make sure no whitespace fields
        email = student['Email Address']
        first_name = student['First Name']
        last_name = student['Last Name']
        stage = student['Stage']
        certification = student['Certification(s)']
        other_certification = student['If Other, indicate certification']
        # print(certification)
        transportation = student['Transportation']
        transport_others = student['Transport Others']
        past_schools = [student['District Code 1'],
                        student['District Code 2'],
                        student['District Code 3'],
                        student['District Code 4']]
        certification = create_student_certifications(certification, other_certification)
        # print(certification)
        if stage == 'Stage 1 & 2':
            preferred_time = student['Preferred Time']
            alternate_times = student['Alternate Time']
            other_preferred_time = student['If Other, indicate preferred lab time']
            other_alternate_times = student['If Other, indicate alternate lab time']

            new_student = Stage1And2Student(email=email,
                                            name=first_name + ' ' + last_name,
                                            certifications=certification,
                                            transportation=transportation == 'Yes',
                                            transport_others=transport_others == 'Yes',
                                            preferred_lab_time=create_time(preferred_time, other_preferred_time),
                                            alt_lab_times=create_times(alternate_times, other_alternate_times),
                                            past_schools=past_schools)
            stage_1_and_2_students.append(new_student)

        elif stage == 'Stage 3':
            time_260 = student['260 Time']
            other_time_260 = student['If Other, indicate EDUC 260 lab time']
            time_360 = student['360-366 Time']
            other_time_360 = student['If Other, indicate EDUC 360-366 lab time']
            time_368 = student['368 Time'] 
            other_time_368 = student['If Other, indicate EDUC 368 lab time']
            time_3582 = student['358.2 Time']
            other_time_3582 = student['If Other, indicate EDUC 358.2 lab time']

            lab_times = create_times(time_260, other_time_260) + create_times(time_360, other_time_360) + \
                        create_times(time_368, other_time_368) + create_times(time_3582, other_time_3582)

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
    for teacher in teachers:
        # Just need to check to make sure no whitespace fields
        email = teacher['Email Address']
        name = teacher['Teacher\'s Full Name']
        school = teacher['District/Entity']
        subject = teacher['Subject']
        grade = teacher['Grade']
        stage_3_times = teacher['Stage 3 Lab']
        other_stage_3_times = teacher['If Other, indicate Stage 3 lab time']
        stage_1_and_2_times = teacher['Stage 1 & 2 Lab']
        other_stage_1_and_2_times = teacher['If Other, indicate Stage 1 & 2 lab time']

        new_teacher = Teacher(email=email,
                              name=name,
                              school=school,
                              certification=Certification(subject=subject, grades=convert_grade(grade)),
                              stage2_times=create_times(stage_1_and_2_times, other_stage_1_and_2_times),
                              stage3_times=create_times(stage_3_times, other_stage_3_times))

        teacher_list.append(new_teacher)
    
    return teacher_list


def check_certification(student, teacher):
    """
    Check if teacher grade and subject are in one of the student's certifications
    """
    student_certifications = student.get_certifications()
    teacher_certification = teacher.get_certification()
    teacher_subject = teacher_certification.get_subject()
    print('teacher subject:', teacher_subject)
    teacher_grade = teacher_certification.get_grades()
    print('teacher grade:', teacher_grade)

    # for cert in student_certifications:
    #     print('student cert:', cert)
    #     # print('cert subject:', cert.get_subject())
    #     # print('cert grade:', cert.get_grades())
    #     if cert.get_subject() == teacher_subject and all(grade in cert.get_grades() for grade in teacher_grade):
    #         return True

    # return False

    # return any([cert.get_subject() == teacher_subject and 
    #             all(grade in cert.get_grades() for grade in teacher_grade) 
    #             for cert in student.get_certifications()])

    # Use filter to return time if needed
    return list(filter(lambda cert: cert.get_subject() == teacher_subject and all(grade in cert.get_grades() for grade in teacher_grade), 
                       student.get_certifications()))


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
    return any(time in teacher.get_stage2_times() for time in student.get_alternate_times())
    # return list(filter(lambda ele: ele in teacher.get_stage2_times(), student.get_alternate_times()))
    

def check_stage_3_times(student, teacher):
    """
    Only used for stage 3 students for there lab times
    This function is used first before stage 1 & 2 students are considered
    """
    student_times = student.get_lab_times()
    teacher_times = teacher.get_stage3_times()
    # print(student_times)
    # print(teacher_times[1])
    # for time in student_times:
    #     print(time)
    #     if time in teacher_times:
    #         return True

    # return False
    return any(time in teacher.get_stage3_times() for time in student.get_lab_times())
    # Use filter to return time if needed
    # return list(filter(lambda time: time in teacher.get_stage3_times(), student.get_lab_times()))

def check_school(student, teacher):
    """Check that the teacher's school is not in the students list of previous schools"""
    return teacher.get_school() in student.get_past_schools()
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
    certification = check_certification(student, teacher)
    print(certification)
    school = check_school(student, teacher)
    print(school)
    teacher_is_taken = teacher.get_match_found()
    student_can_commute = check_transport(student, teacher)
    print(student_can_commute)
    if isinstance(student, Stage3Student):
        lab_time = check_stage_3_times(student, teacher)
        print(lab_time)
    elif isinstance(student, Stage1And2Student) and alternate_time:
        pass
    else:
        pass
    # availability = check_availability(student, teacher) # Change based on which instance is passed in
    

    # return subject and grade and availability and not school and not teacher_is_taken, student_can_commute
    return 0, 1
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
    # for student in students:
    #     for teacher in teachers:
    student_matches_teacher, student_can_commute = perform_checks(students[0], teachers[0], alternate_time)
            
    #         if student_matches_teacher:
    #             match_found(student, teacher)

    #             if not student_can_commute:
    #                 students_need_ride.append(student)
    
    # assign_drivers(students_need_ride, students)
    # print_sched(teachers)


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
    stage_1_and_2_students, stage_3_students = make_students("Student Field Experiences.csv")
    teachers = make_teachers("Teacher Field Experiences.csv")
    for student in stage_1_and_2_students:
        print()
        print(student)
    for student in stage_3_students:
        print()
        print(student)

    print()
    for teacher in teachers:
        print(teacher)

    print()
    matchmaker(stage_3_students, teachers)
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