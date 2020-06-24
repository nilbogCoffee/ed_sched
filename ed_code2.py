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
                          can_drive=student[fieldnames[4]] == 'T',
                          experience=student[fieldnames[5]].split(','))
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
                          can_walk=teacher[fieldnames[5]] == 'T')
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


def print_sched(student, teacher):
    """Print the schedule results"""
    if not check_transport(student, teacher):
        print(student.get_name() + " will join " + teacher.get_name() + ". Needs to find a ride.")
    else:
        print(student.get_name() + " will join " + teacher.get_name())


def matchmaker(students, teachers):
    """
    Determines which students are matches with each teacher by each student object attribute
    """
    for student in students:
        for teacher in teachers:
            subject = check_subject(student, teacher)
            grade = check_grade(student, teacher)
            availability = check_availability(student, teacher)
            school = check_school(student, teacher)
            teacher_is_taken = teacher.get_match_found()
            
            if subject and grade and availability and not school and not teacher_is_taken:
                print_sched(student, teacher)
                teacher.set_match_found(True)
                student.set_match_found(True)
                teacher.set_student(student)


def write_schedule(teachers):
    """Write results to csv file"""
    with open("sched.csv", "w") as schedule:
        writer = csv.DictWriter(schedule, fieldnames=["Student", "Teacher", "School", "Lab"])
        writer.writeheader()

        for teacher in teachers:
            if teacher.get_student() is not None:
                writer.writerow({"Student": teacher.get_student().get_name(), "Teacher": teacher.get_name(), "School": teacher.get_school(),"Lab": teacher.get_availability()})


def write_extra_students(students):
    """Write the students that have no assigned field experience to a csv file"""
    with open("unmatched_students.csv", "w") as schedule:
        writer = csv.DictWriter(schedule, fieldnames=["Student","Lab", "Can Drive"])
        writer.writeheader()

        for student in students:
            if not student.get_match_found():
                writer.writerow({"Student": student.get_name(), "Lab": student.get_availability(), "Can Drive": student.get_can_drive()})


def main():
    students = make_students("Tidy_Ed_Data_Students.csv")
    teachers = make_teachers("Tidy_Ed_Data_Teachers.csv")
    for student in students:
        print(student)

    print()
    for teacher in teachers:
        print(teacher)

    print()
    matchmaker(students, teachers)

    write_schedule(teachers)
    write_extra_students(students)


if __name__ == '__main__':
    main()

