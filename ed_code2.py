import csv
from classes import Student, Teacher

def make_students(file_name):
    """
    Create all student objects from the Tidy_Ed_Data_Teachers.csv file
    """
    student_list = []
    students = csv.DictReader(open(file_name, encoding='utf-8-sig'))   # Need encoding field to delete the Byte Order Mark (BOM)
    fieldnames = students.fieldnames   # Gets the fieldnames from the csv file so we do not have to hardcode values
    for student in students:
        student = Student(name=student[fieldnames[0]],
                          subject=student[fieldnames[1]],
                          grades=student[fieldnames[2]].split(','),
                          availability=student[fieldnames[3]].split(','),
                          can_drive=student[fieldnames[4]] == 'Yes',
                          can_car_pool=student[fieldnames[5]] == 'Yes',
                          experience=student[fieldnames[6]].split(','))
        student_list.append(student)
    
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
    """Perform all checks between student and teacher to see if they are compatible"""
    subject = check_subject(student, teacher)
    grade = check_grade(student, teacher)
    availability = check_availability(student, teacher)
    school = check_school(student, teacher)
    teacher_is_taken = teacher.get_match_found()
    can_get_there = check_transport(student, teacher)

    return subject, grade, availability, school, teacher_is_taken, can_get_there


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
    needs_a_ride = []
    for student in students:
        for teacher in teachers:
            subject, grade, availability, school, teacher_is_taken, can_get_there = perform_checks(student, teacher)
            
            if subject and grade and availability and not school and not teacher_is_taken:
                match_found(student, teacher)

                if not can_get_there:
                    needs_a_ride.append(student)
    
    assign_drivers(needs_a_ride, students)
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
            if teacher.get_student() is not None:
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
    students = make_students("Tidy_Ed_Data_Students.csv")
    teachers = make_teachers("Tidy_Ed_Data_Teachers.csv")
    for student in students:
        print(student)

    # print()
    # for teacher in teachers:
    #     print(teacher)

    # print()
    matchmaker(students, teachers)

    write_schedule(teachers)
    write_extra_students(students)


if __name__ == '__main__':
    main()

