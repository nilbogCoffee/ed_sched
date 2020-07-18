import csv
# import run_program_GUI
from classes import Teacher, Certification, LabTime, Stage1And2Student, Stage3Student

def createCertifications(certification): #There are semi-colons in the csv from forms
    certification_list = []
    certifications = certification.split(',')
    for cert in certifications:
        if cert == 'Other':
            certification_list.append('Other')
        else:
            subject = cert[cert.rfind(' ') + 1:]
            print(subject)
            grades = cert[cert.find('(') + 8 : cert.find(')')]
            if grades[0] == 'K':
                grades[0] = '0'
            elif grades[0] == 'PK':
                grades[0] = '-1'
            print(grades)
            grades = grades.split('-')
            grades = list(range(int(grades[0]), int(grades[-1]) + 1))
            print(grades)
            certification_list.append(Certification(subject=subject, grades=grades))
        
    return certification_list


def createTimes(times, end_index):
    times = times.split(',')
    lab_times =[]
    for time in times:
        print(time)
        if 'None' not in time:
            days = time[7:end_index].split('/')
            print(days)
            time = time[end_index+1:]
            print(time)
            lab_time = LabTime(days=days, time=time)
            print(lab_time)
            lab_times.append(lab_time)

    return lab_times


def make_students(file_name):
    """
    Create all student objects from the Tidy_Ed_Data_Teachers.csv file
    """
    student_list = []
    students = csv.DictReader(open(file_name, encoding='utf-8-sig'))   # Need encoding field to delete the Byte Order Mark (BOM)
    for student in students:
        print('\n new student incoming \n')
        email = student['Email Address']
        first_name = student['First Name']
        last_name = student['Last Name']
        stage = student['Stage']
        certification = student['Certification(s)']
        transportation = student['Transportation']
        transport_others = student['Transport Others']
        past_schools = [student['School 1'].lower(), 
                        student['School 2'].lower(), 
                        student['School 3'].lower(), 
                        student['School 4'].lower()]

        certification = createCertifications(certification)

        if stage == 'Stage 1 & 2':
            preferred_time = student['Preferred Time']
            alternate_times = student['Alternate Time']
            all_times = preferred_time + ',' + alternate_times
            lab_times = createTimes(all_times, 9)

            new_student = Stage1And2Student(email=email,
                                            name=first_name + ' ' + last_name,
                                            certifications=certification,
                                            transportation=transportation == 'Yes',
                                            transport_others=transport_others == 'Yes',
                                            preferred_lab_time=lab_times[0],
                                            alt_lab_times = lab_times[1:],
                                            past_schools=past_schools)

            print(new_student)
        elif stage == 'Stage 3':
            time_260 = student['260 Time']
            time_360 = student['360-366 Time']
            time_368 = student['368 Time']
            time_3582 = student['358.2 Time']
            lab_times = []

            if time_260:
                lab_times += createTimes(time_260, 9)

            if time_360:
                lab_times += createTimes(time_360, 16)

            if time_368:
                lab_times += createTimes(time_368,12)

            if time_3582:
                times = time_3582.split(',')
                for time in times:
                    if 'A' in time:
                        days = time[7:12].split('/')
                        lab_time = time[13:]
                    else:
                        days = time[7:9]
                        lab_time = time[10:]
                    lab_times += LabTime(days=days, time=lab_time)
            
            new_student = Stage3Student(email=email,
                                        name=first_name + ' ' + last_name,
                                        certifications=certification,
                                        transportation=transportation == 'Yes',
                                        transport_others=transport_others == 'Yes',
                                        lab_times=lab_times,
                                        past_schools=past_schools)

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
    students = make_students("Field Experiences.csv")
    # teachers = make_teachers("Tidy_Ed_Data_Teachers.csv")
    for student in students:
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