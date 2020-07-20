import csv
from classes import Teacher, Certification, LabTime, Stage1And2Student, Stage3Student

def create_certifications(certification): #There are semi-colons in the csv from forms
    """
    Create certification objects from a list of certifications from a student using their certified grades and subjects
    """
    return [create_certification(cert) for cert in certification.split(', ')]


def create_certification(certification):
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


def create_times(times, end_index):
    """
    Create lab time objects based on the day and time of the list of labs from a student
    """
    return [create_time(time, end_index) for time in times.split(', ') if times and 'None' not in time]


def create_time(time, end_index):
    """
    Create a single LabTime object based on the day and time of the lab
    """
    def get_days():
        return time[7:end_index].split('/')

    def get_time():
        return time[end_index+1:]
    
    return LabTime(days=get_days(), time=get_time())


def make_students(file_name):
    """
    Create all student objects from the file
    """
    student_list = []
    students = csv.DictReader(open(file_name, encoding='utf-8-sig'))   # Need encoding field to delete the Byte Order Mark (BOM)
    for student in students:
        email = student['Email Address']
        first_name = student['First Name']
        last_name = student['Last Name']
        stage = student['Stage']
        certification = student['Certification(s)']
        transportation = student['Transportation']
        transport_others = student['Transport Others']
        past_schools = [student['School 1'], student['School 2'], student['School 3'], student['School 4']]

        certification = create_certifications(certification)

        if stage == 'Stage 1 & 2':
            all_lab_times = student['Preferred Time'] + ', ' + student['Alternate Time']
            lab_times = create_times(all_lab_times, 10)

            new_student = Stage1And2Student(email=email,
                                            name=first_name + ' ' + last_name,
                                            certifications=certification,
                                            transportation=transportation == 'Yes',
                                            transport_others=transport_others == 'Yes',
                                            preferred_lab_time=lab_times[0],
                                            alt_lab_times = lab_times[1:],
                                            past_schools=list(map(lambda school: school.lower(), past_schools)))

        elif stage == 'Stage 3':
            time_260 = student['260 Time']
            time_360 = student['360-366 Time']
            time_368 = student['368 Time']
            time_3582 = student['358.2 Time']
            lab_times = create_times(time_260, 10) + create_times(time_360, 16) + create_times(time_368,12)

            for time in time_3582.split(','):
                if 'A' in time:
                    lab_times.append(create_time(time, 12))
                elif time:
                    lab_times.append(create_time(time, 10))
            
            new_student = Stage3Student(email=email,
                                        name=first_name + ' ' + last_name,
                                        certifications=certification,
                                        transportation=transportation == 'Yes',
                                        transport_others=transport_others == 'Yes',
                                        lab_times=lab_times,
                                        past_schools=list(map(lambda school: school.lower(), past_schools)))

        student_list.append(new_student)

    return student_list


def make_teachers(file_name):
    """
    Create all teacher objects from the Tidy_Ed_Data_Students.csv file
    """
    teacher_list = []
    teachers = csv.DictReader(open(file_name, encoding='utf-8-sig'))   # Need encoding field to delete the Byte Order Mark (BOM)
    fieldnames = teachers.fieldnames    # Gets the fieldnames from the csv file so we do not have to hardcode values
    for teacher in teachers:
        teacher = Teacher(name=teacher[fieldnames[0]],
                          subject=teacher[fieldnames[1]],
                          grade=teacher[fieldnames[2]],
                          school=teacher[fieldnames[3]],
                          availability=teacher[fieldnames[4]],
                          can_walk=teacher[fieldnames[5]] == 'Yes')
        teacher_list.append(teacher)
    
    return teacher_list


def check_subject(student, teacher):
    """Check the student and teacher subjects are equal"""
    return student.get_subject() == teacher.get_subject()


def check_grade(student, teacher):
    """Check that the teacher grade is in the student's certified grades"""
    return teacher.get_grade() in student.get_grades()


def check_availability(student, teacher):
    """Check that the teacher's availability is in the student's availability"""
    return teacher.get_availability() in student.get_availability()


def check_school(student, teacher):
    """Check that the teacher's school is not in the students list of previous schools"""
    return teacher.get_school() in student.get_experience()


def check_transport(student, teacher):
    """Check that the student can drive or walk"""
    return student.get_can_drive() or teacher.get_can_walk()


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


def perform_checks(student, teacher):
    """
    Perform all checks between student and teacher to see if they are compatible
    Returns a tuple of whether the match is found and whether the student can commute
    """
    subject = check_subject(student, teacher)
    grade = check_grade(student, teacher)
    availability = check_availability(student, teacher)
    school = check_school(student, teacher)
    teacher_is_taken = teacher.get_match_found()
    student_can_commute = check_transport(student, teacher)

    return subject and grade and availability and not school and not teacher_is_taken, student_can_commute


def match_found(student, teacher):
    """Match found between student and teacher. Sets the teacher's student. Overwrites the student's availability"""
    teacher.set_match_found(True)
    student.set_match_found(True)
    teacher.set_student(student)
    student.set_availability(teacher.get_availability())  # Overwrite the student's availability to the teacher's availability


def matchmaker(students, teachers):
    """
    Determines which students are matches with each teacher by each student object attribute
    This is the main function that this program is centered around
    """
    students_need_ride = []
    for student in students:
        for teacher in teachers:
            student_matches_teacher, student_can_commute = perform_checks(student, teacher)
            
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
    students = make_students("sheetsFile.csv")
    # teachers = make_teachers("Tidy_Ed_Data_Teachers.csv")
    for student in students:
        print()
        print(student)

    # print()
    # for teacher in teachers:
    #     print(teacher)

    # print()
    # matchmaker(students, teachers)

    # write_schedule(teachers)
    # write_extra_students(students)


if __name__ == '__main__':
    main()


"""
TODO:
1. Ask Mrs. Correll to fix the original file with correct headers and proper formatting (Google Form)
2. Make another file called Main that runs the program and remove the main function from this file
3. Write bash script to actually run the program so that a user can execute program on double click of the bash script
4. Add GUI so that user can choose files from their Finder Menu (This is partially done. Not visually appealing)
"""