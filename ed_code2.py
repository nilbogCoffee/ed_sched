from classes import Student, Teacher


def make_students(file_name):
    student_list = []
    with open(file_name, 'rt') as reader:
        lines = reader.readlines()
    lines.pop(0)
    for student in lines:
        student = student.strip()
        student = student.split(',')
        student = Student(name=student[0],
                          subject=student[1],
                          grades=student[2].split(';'),
                          availability=student[3].split(';'),
                          can_drive=student[4],
                          experience=student[5].split(';'))
        student_list.append(student)
    
    return student_list


def make_teachers(file_name):
    teacher_list = []
    with open(file_name, 'rt') as reader:
        lines = reader.readlines()
    lines.pop(0)
    for teacher in lines:
        teacher = teacher.strip()
        teacher = teacher.split(',')
        teacher = Teacher(name=teacher[0],
                          subject=teacher[1],
                          grade=teacher[2],
                          school=teacher[3],
                          availability=teacher[4],
                          can_walk=teacher[5])
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
