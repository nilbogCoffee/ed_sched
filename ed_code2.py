import csv
from openpyxl import Workbook
from classes import Teacher, Certification, LabTime, Stage1And2Student, Stage3Student, Student

def create_student_certifications(certification, other): #There are semi-colons in the csv file downloaded from Google forms
    """
    Create certification objects from a list of certifications from a student using their certified grades and subjects
    :param certification: A string where each subject-grade pair is delimited by a comma
    :param other: A string representing the student's other option
    :returns: A list of Certification objects and other options if other was specified
    """
    return [create_student_certification(cert, other) for cert in certification.split(', ')]


def create_student_certification(certification, other):
    """
    Creates one certification object from subject and grade or returns other options if specified
    :param certification: A string representing a single subject-grade pair used to create a Certification object
    :param other: A string representing the student's other option which cannot be used to create a Certification object
    :returns: A Certification object unless other option is specified, then return other
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


def create_times(times, other):
    """
    Create LabTime objects based on the day and time of the list of labs from a student
    :param times: A string where each day-time pair is delimited by a comma
    :param other: A string representing the student's other option
    :returns: A list of LabTime objects and other options if other is specified
    """
    return [create_time(time, other) for time in times.split(', ') if times]


def create_time(time, other):
    """
    Create a single LabTime object based on the day and time of the lab
    :param time: A string representing a single day-time pair used to create a LabTime object
    :param other: A string representing the student's other option which cannot be used to create a LabTime object
    :returns: A new LabTime object unless other was specified, then return other
    """
    end_index = time.rfind(' ')
    def get_days():
        return time[time.find(':')+2 : end_index].split('/')

    def get_time():
        return time[end_index+1:]

    
    return LabTime(days=get_days(), time=get_time()) if time != 'Other' else other


def convert_grade(grade):
    """
    Converts the teacher's grade
    :param grade: A string of the grade the teacher teaches
    :returns: A list of the new grades
    """
    if grade.startswith('PK'):
        grade = [-1]
    elif grade == 'Kindergarten':
        grade = [0]
    elif grade[:2].isdigit():
        grade = [int(grade[:2])]
    elif grade[:1].isdigit():
        grade = [int(grade[:1])]
    elif grade.startswith('Special'):
        grade = list(range(-1, 13))
    else:
        grade = [grade]
    
    return grade


def make_students(file_name):
    """
    Create all student objects from the Student csv file
    :param file_name: The student file to extract data from using the csv module's DictReader
    :returns: A two element tuple of Stage1And2Student objects and Stage3Student objects
    """
    stage_1_and_2_students = []
    stage_3_students = []
    students = csv.DictReader(open(file_name, encoding='utf-8-sig'))   # Need encoding field to delete the Byte Order Mark (BOM)
    for student in students:
        email = student['Email Address'].strip()
        first_name = student['First Name'].strip()
        last_name = student['Last Name'].strip()
        stage = student['Stage']
        certification = student['Certification(s)']
        other_certification = student['If Other, indicate certification'].strip()
        transportation = student['Transportation']
        transport_others = student['Transport Others']
        transportation_comments = student['Transportation Comments'].strip()
        past_schools = [student['District Code 1'],
                        student['District Code 2'],
                        student['District Code 3'],
                        student['District Code 4']]
        certification = create_student_certifications(certification, other_certification)

        if stage == 'Stage 1 & 2':
            preferred_time = student['Preferred Time']
            alternate_times = student['Alternate Time']
            other_preferred_time = student['If Other, indicate preferred lab time'].strip()
            other_alternate_times = student['If Other, indicate alternate lab time'].strip()
            lab_comments = student['Stage 1&2 Lab Comments'].strip()

            new_student = Stage1And2Student(email=email,
                                            name=first_name + ' ' + last_name,
                                            certifications=certification,
                                            transportation=transportation == 'Yes',
                                            transport_others=transport_others == 'Yes',
                                            preferred_lab_time=create_time(preferred_time, other_preferred_time),
                                            alt_lab_times=create_times(alternate_times, other_alternate_times),
                                            past_schools=past_schools,
                                            transportation_comments=transportation_comments,
                                            lab_comments=lab_comments)
            stage_1_and_2_students.append(new_student)

        elif stage == 'Stage 3':
            time_260 = student['260 Time']
            other_time_260 = student['If Other, indicate EDUC 260 lab time'].strip()
            time_360 = student['360-366 Time']
            other_time_360 = student['If Other, indicate EDUC 360-366 lab time'].strip()
            time_368 = student['368 Time'] 
            other_time_368 = student['If Other, indicate EDUC 368 lab time'].strip()
            time_3582 = student['358.2 Time']
            other_time_3582 = student['If Other, indicate EDUC 358.2 lab time'].strip()
            lab_comments = student['Stage 3 Lab Comments'].strip()

            lab_times = create_times(time_260, other_time_260) + create_times(time_360, other_time_360) + \
                        create_times(time_368, other_time_368) + create_times(time_3582, other_time_3582)

            new_student = Stage3Student(email=email,
                                        name=first_name + ' ' + last_name,
                                        certifications=certification,
                                        transportation=transportation == 'Yes',
                                        transport_others=transport_others == 'Yes',
                                        lab_times=lab_times,
                                        past_schools=past_schools,
                                        transportation_comments=transportation_comments,
                                        lab_comments=lab_comments)

            stage_3_students.append(new_student)

    return stage_1_and_2_students, stage_3_students


def make_teachers(file_name):
    """
    Create all teacher objects from the Teacher csv file
    :param file_name: The file to extract data from using the csv module's DictReader
    :returns: A list of Teacher objects
    """
    teacher_list = []
    teachers = csv.DictReader(open(file_name, encoding='utf-8-sig'))   # Need encoding field to delete the Byte Order Mark (BOM)
    for teacher in teachers:
        email = teacher['Email Address'].strip()
        name = teacher['Teacher\'s Full Name'].strip()
        school = teacher['District/Entity']
        subject = teacher['Subject']
        grade = teacher['Grade']
        stage_3_times = teacher['Stage 3 Lab']
        other_stage_3_times = teacher['If Other, indicate Stage 3 lab time'].strip()
        stage_1_and_2_times = teacher['Stage 1 & 2 Lab']
        other_stage_1_and_2_times = teacher['If Other, indicate Stage 1 & 2 lab time'].strip()

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
    :param student: The Student object
    :param teacher: The Teacher object
    :returns: Boolean value
    """
    student_certifications = student.get_certifications()
    teacher_certification = teacher.get_certification()
    teacher_subject = teacher_certification.get_subject()
    teacher_grade = teacher_certification.get_grades()

    return any(cert.get_subject() == teacher_subject and 
                all(grade in cert.get_grades() for grade in teacher_grade) 
                for cert in student_certifications)


def check_stage_1_and_2_preferred(student, teacher):
    """
    Only used for stage 1 and 2 students for preferred times.
    This function will be used after stage 3 students are handled
    :param student: The Student object
    :param teacher: The Teacher object
    :returns: A single element list of the student preferred time if that time is in teacher times, otherwise empty string
    """
    return [student.get_preferred_lab_time()] if student.get_preferred_lab_time() in teacher.get_stage2_times() else ''


def check_stage_1_and_2_alternate(student, teacher):
    """
    Only used for stage 1 and 2 students for there alternate times
    This function is used after preferred times are handled for all students
    :param student: The Student object
    :param teacher: The Teacher object
    :eturns: A list of all student alternate times that are in the teacher times
    """
    return [time for time in student.get_alt_lab_times() if time in teacher.get_stage2_times()]


def check_stage_3_times(student, teacher):
    """
    Only used for stage 3 students for there lab times
    This function is used first before stage 1 & 2 students are considered
    :param student: The Student object
    :param teacher: The Teacher object
    :returns: A list of all student times that are in the teacher times
    """
    return [time for time in student.get_lab_times() if time in teacher.get_stage3_times()]


def check_school(student, teacher):
    """
    Check that the teacher's school is not in the students list of previous schools
    :param student: The Student object
    :param teacher: The Teacher object
    :returns: Boolean result
    """
    return teacher.get_school() in student.get_past_schools()


def check_transport(student, teacher):
    """
    Check that the student can commute
    :param student: The Student object
    :param teacher: The Teacher object
    :returns: boolean result
    """
    return student.get_transportation()


def print_sched(teachers):
    """
    Print the schedule results
    Used for debugging
    :param teachers: A list of Teacher objects 
    """
    for teacher in teachers:
        student = teacher.get_student()
        student_name = student.get_name()
        teacher_name = teacher.get_name()
        subject = teacher.get_certification().get_subject()
        grades = ', '.join(map(str, teacher.get_certification().get_grades()))
        lab_times = ', '.join(map(str, teacher.get_all_lab_times()))
        if student.get_other_drivers():
            print(f"{student_name} will join {teacher_name}, teaching {subject} to grade {grades} at any of these times: {lab_times}. Also, {student_name} should get a ride from one of the following:", 
                   ', '.join(driver.get_name() for driver in student.get_other_drivers()))
        elif not student.get_transportation() and not student.get_other_drivers():
            print(f"{student_name} will join {teacher_name}, teaching {subject} to grade {grades} at any of these times: {lab_times}. Also, {student_name} will need a ride.")
        else:
            print(f"{student_name} will join {teacher_name}, teaching {subject} to grade {grades} at any of these times: {lab_times}")


def perform_checks(student, teacher, alternate_time):
    """
    Perform all checks between student and teacher to see if they are compatible
    :param student: The Student object
    :param teacher: The Teacher object
    :param alternate_time: A boolean value specifying whether or not to use the student's alternate times
    :returns: A four element tuple of all checks
    """
    certification = check_certification(student, teacher)
    school = check_school(student, teacher)
    student_can_commute = check_transport(student, teacher)

    if isinstance(student, Stage3Student):
        lab_time = check_stage_3_times(student, teacher)

    elif isinstance(student, Stage1And2Student) and alternate_time:
        lab_time = check_stage_1_and_2_alternate(student, teacher)

    else:
        lab_time = check_stage_1_and_2_preferred(student, teacher)
    
    return certification, school, lab_time, student_can_commute


def match_found(student, teacher, lab_times):
    """
    Match found between student and teacher. Sets the teacher's student. Overwrites the student's and teachers' lab times
    :param student: The Student object
    :param teacher: The Teacher object
    :param lab_times: The list of lab_times that are the same between student and teacher
    """
    student.set_match_found(True)
    teacher.set_match_found(True)
    teacher.set_student(student)

    if isinstance(student, Stage3Student):
        teacher.set_stage3_times(lab_times)
        teacher.set_stage2_times([])
    else:
        if len(lab_times) == 1 and lab_times[0] == student.get_preferred_lab_time():
            lab_times += check_stage_1_and_2_alternate(student, teacher)
            if lab_times.count(lab_times[0]) > 1:
                lab_times.reverse()
                lab_times.remove(lab_times[0])
                lab_times.reverse()
            
        teacher.set_stage2_times(lab_times)
        teacher.set_stage3_times([])

    student.set_lab_times(lab_times)


def matchmaker(students, teachers, alternate_time=False):
    """
    Determines which students are matches with each teacher by each student object attribute
    Assigns drivers to students that cannot commute
    Prints the schedule results
    This is the main function that this program is centered around
    :param students: A list of student objects
    :param teachers: A list of teacher objects
    :param alternate_time: A boolean value specifying whether or not to use the student's alternate times
    :returns: A list of students that have no matched teacher
    """
    students_need_ride = []
    for student in students:
        for teacher in teachers:
            if not teacher.get_match_found() and not student.get_match_found():
                certification, previous_school, lab_times, can_commute = perform_checks(student, teacher, alternate_time)
                print(certification, previous_school, lab_times, can_commute)
                if certification and lab_times and not previous_school:
                    match_found(student, teacher, lab_times)
                    if not can_commute:
                        students_need_ride.append(student)
                    break

    unmatched_students = [student for student in students if not student.get_match_found()]

    return unmatched_students, students_need_ride


def assign_drivers(students_need_ride, all_students):
    """
    Students that need a ride are given a list of students that are available for car pool
    :param students_need_ride: A list of students that cannot commute
    :param all_students: A list of all students
    """
    print(students_need_ride)
    print(all_students)
    for student in students_need_ride:
       for driver in all_students:
           if any(time in driver.get_lab_times() for time in student.get_lab_times()) and driver.get_transport_others() and driver.get_match_found():
               student.add_driver(driver)


def format_grades(grades):
    """
    Change the -1 and 0 grade values back to 'PK' and 'K'
    :param grades: A list of integer values
    :returns: A new list of grades
    """
    if -1 in grades:
        grades[grades.index(-1)] = 'PK'
    if 0 in grades:
        grades[grades.index(0)] = 'K'

    return grades 


def write_schedule(teachers, workbook):
    """
    Write results to a the schedule sheet in the workbook for the .xlsx file
    :param teachers: A list of Teacher objects
    """
    schedule_sheet = workbook["Schedule"]
    headers = ["Student Name", "Teacher Name", "Stage", "District", "Subject", 
               "Optimal Lab Time", "All Possible Lab Times", 
               "Grade", "Transportation", "Transport Others", "Potential Drivers",
               "Transportation Comments", "Lab Comments"]
    schedule_sheet.append(headers)

    for teacher in teachers:
        if teacher.get_match_found():                
            student = teacher.get_student()
            lab_times = teacher.get_all_lab_times()
            optimal = str(lab_times[0]) if isinstance(student, Stage1And2Student) and student.get_preferred_lab_time() == lab_times[0] else ''
            schedule_sheet.append([student.get_name(),
                                   teacher.get_name(),
                                   'Stage 1 & 2' if isinstance(student, Stage1And2Student) else 'Stage 3',
                                   teacher.get_school(),
                                   teacher.get_certification().get_subject(),
                                   optimal,
                                   ', '.join(map(str, lab_times)),
                                   ', '.join(map(str, format_grades(teacher.get_certification().get_grades()))),
                                   'Yes' if student.get_transportation() else 'No',
                                   'Yes' if student.get_transport_others() else 'No',
                                   ', '.join(map(Student.get_name, student.get_other_drivers())) if student.get_other_drivers() else '',
                                   student.get_transportation_comments(),
                                   student.get_lab_comments()
                                   ])


def write_unmatched_students(students, workbook):
    """
    Write the students that have no assigned field experience to a csv file
    Write students that have no assigned field experience to the unmatched students sheet in the workbook for the .xlsx file
    :param students: A list of Student objects
    """
    unmtached_students_sheet = workbook["Unmatched Students"]
    headers = ["Student Name", "Stage", "Transportation", "Transport Others",
               "Transportation Comments", "Certifications", "Labs", "Lab Comments"]
    unmtached_students_sheet.append(headers)

    for student in students:
        for certification in student.get_certifications():
            format_grades(certification.get_grades())
        unmtached_students_sheet.append([student.get_name(),
                                         'Stage 1 & 2' if isinstance(student, Stage1And2Student) else 'Stage 3',
                                         'Yes' if student.get_transportation() else 'No',
                                         'Yes' if student.get_transport_others() else 'No',
                                         student.get_transportation_comments(),
                                         ', '.join(map(str, student.get_certifications())),
                                         ', '.join(map(str, student.get_lab_times())),
                                         student.get_lab_comments()
                                         ])


def make_workbook():
    """
    Create the .xlsx file workbook with two sheets for the final schedule and unmatched students
    :returns: The new workbook object
    """
    workbook = Workbook()
    schedule_sheet = workbook.active
    unmatched_students_sheet = workbook.create_sheet()
    schedule_sheet.title = "Schedule"
    unmatched_students_sheet.title = "Unmatched Students"
    
    return workbook

# def main():
#     stage_1_and_2_students, stage_3_students = make_students("Testing_All_Student_Fields.csv")
#     teachers = make_teachers("Testing_All_Teacher_Fields.csv")
#     for student in stage_1_and_2_students:
#         print(student)
#         print()
#     for student in stage_3_students:
#         print(student)
#         print()

#     # # print()
#     for teacher in teachers:
#         print(teacher)
#         print()

#     stage_3_leftover, stage_3_need_ride = matchmaker(stage_3_students, teachers)
#     matchmaker(stage_1_and_2_students, teachers)
#     stage_1_and_2_leftover, stage_1_and_2_need_ride = matchmaker(stage_1_and_2_students, teachers, alternate_time=True)

#     assign_drivers(stage_3_need_ride + stage_1_and_2_need_ride, stage_1_and_2_students + stage_3_students)
#     workbook = make_workbook()
#     write_schedule(teachers, workbook)
#     write_unmatched_students(stage_3_leftover + stage_1_and_2_leftover, workbook)
#     workbook.save(os.path.expanduser('~') + '/Downloads/Schedule.xlsx')


# if __name__ == '__main__':
#     main()
