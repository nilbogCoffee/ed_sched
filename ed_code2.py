import csv
from classes import Student, Teacher

def make_students(file_name):
    """
    Create all student objects from the Tidy_Ed_Data_Teachers.csv file
    """
    student_list = []
    students = csv.DictReader(open(file_name, encoding='utf-8-sig'))   # Need encoding field to delete the Byte Order Mark (BOM)
    for student in students:
        student = Student(name=student['Student_Name'],
                          subject=student['Subject'],
                          grades=student['Grades'].split(';'),
                          availability=student['Availability'].split(';'),
                          can_drive=student['Can_Drive'] == 'T',
                          experience=student['Previous'].split(';'))
        student_list.append(student)
    
    return student_list


def make_teachers(file_name):
    """
    Create all teacher objects from the Tidy_Ed_Data_Students.csv file
    """
    teacher_list = []
    teachers = csv.DictReader(open(file_name, encoding='utf-8-sig'))   # Need encoding field to delete the Byte Order Mark (BOM)
    for teacher in teachers:
        teacher = Teacher(name=teacher['Teacher_Name'],
                          subject=teacher['Subject'],
                          grade=teacher['Grade'],
                          school=teacher['School_Code'],
                          availability=teacher['Availability'],
                          can_walk=teacher['Can_Walk'] == 'T')
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


def print_sched(student, teacher, transport):
    """Print the schedule results"""
    if not transport:
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
            if subject:
                grade = check_grade(student, teacher)
                if grade:
                    availability = check_availability(student, teacher)
                    if availability:
                        school = check_school(student, teacher)
                        if not school:
                            transport = check_transport(student, teacher)
                            print_sched(student, teacher, transport)
                            teacher.set_availability("N/A")
                            break


def main():
    students = make_students("Tidy_Ed_Data_Students.csv")
    teachers = make_teachers("Tidy_Ed_Data_Teachers.csv")
    for student in students:
        print(student)

    print()
    for teacher in teachers:
        print(teacher)
    matchmaker(students, teachers)

if __name__ == '__main__':
    main()
