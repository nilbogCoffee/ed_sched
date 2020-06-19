import csv
from classes import Student, Teacher

def make_students(file_name):
    """
    Create all student objects from the Tidy_Ed_Data_Teachers.csv file
    """
    student_list = []
    students = csv.DictReader(open(file_name, encoding='utf-8-sig'))
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
    teachers = csv.DictReader(open(file_name, encoding='utf-8-sig'))
    for teacher in teachers:
        teacher = Teacher(name=teacher['Teacher_Name'],
                          subject=teacher['Subject'],
                          grade=teacher['Grade'],
                          school=teacher['School_Code'],
                          availability=teacher['Availability'],
                          can_walk=teacher['Can_Walk'] == 'T')
        teacher_list.append(teacher)
    
    return teacher_list


def main():
    students = make_students("Tidy_Ed_Data_Students.csv")
    teachers = make_teachers("Tidy_Ed_Data_Teachers.csv")
    for student in students:
        print(student)

    print()
    for teacher in teachers:
        print(teacher)

if __name__ == '__main__':
    main()
