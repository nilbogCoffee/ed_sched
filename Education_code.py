#This is the start of the Education Student Placement project

#This Code made by Steven Berger and Shane Houghton
#We used a subset of Mrs. Correll's original data and tidied it in the files:
#Tidy_Ed_Data_Teachers and Tidy_Ed_Data_Students

#We finished the part of the code that reads in the files; need to finish the main function that creates the matches.


def make_student_dictionary(file):
    infile = open(file,"rt")
    Student_Dictionary = {}
    Line_list = []
    Skip_Line = True
    for line in infile:
        if Skip_Line:
            Skip_Line = False
        else:
            line = line.strip()
            Line_list.append(line)

    for element in Line_list:
        element = element.split(",")
        # for piece in element:
        #     piece = piece.strip("[")
        #     piece = piece.split(";")
        #     print(piece)

        # element[1] = element[1].split(";")
        # element[2] = element[2].split(";")
        # element[3] = element[3].split(";")
        # element[6] = element[6].split(";")
        Student_Dictionary[element[0]] = element[1:]

    for element in Student_Dictionary:
        for thing in Student_Dictionary[element]:
            thing = thing.split(';')

    infile.close()
    return Student_Dictionary

def make_teacher_dictionary(file):
    infile = open(file, "rt")
    Teacher_Dictionary = {}
    Line_list = []
    Skip_Line = True
    for line in infile:
        if Skip_Line:
            Skip_Line = False
        else:
            line = line.strip()
            Line_list.append(line)
    for element in Line_list:
        element = element.split(",")
    #     element[3] = element[3].split(";")
    #     element[4] = element[4].split(";")
    #     element[5] = element[5].split(";")
        Teacher_Dictionary[element[0]] = element[1:]

    infile.close()
    return Teacher_Dictionary



#Outer Loop for Students
    #Inner Loop for Teachers
        #Check for walking distance, lab times, grade, subject
        #We need to do iterative comparisons because we have lists of lists

def compare_lists(student_list, teacher_list):
    # print(student_list)
    # print(teacher_list)
    Match_found = False
    for element in student_list:
        for i in teacher_list:
            if element == i:
                Match_found = True
                return Match_found,i
    return (Match_found, "None")



#Need to finish this Main function to actually make the placements
def main():
    student_dictionary = make_student_dictionary("Tidy_Ed_Data_Students.csv")
    teacher_dictionary = make_teacher_dictionary("Tidy_Ed_Data_Teachers.csv")
    for a in student_dictionary:
        print(a, student_dictionary[a])

    print('teacher\n')
    for a in teacher_dictionary:
        print(a, teacher_dictionary[a])
    # not_available_teachers = []

    for student in student_dictionary:
        for teacher in teacher_dictionary:

            a,b =compare_lists(student_dictionary[student][0], teacher_dictionary[teacher][3])  # checking if the subject matches
            if a:
                print(student)
                print(teacher)
                print(b)

                a,b =compare_lists(student_dictionary[student][1], teacher_dictionary[teacher][2])
                if a:
                    print(b)

                    a, b = compare_lists(student_dictionary[student][1], teacher_dictionary[teacher][2])
                    if a:
                        print(b)



main()


