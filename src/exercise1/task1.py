import curses
import os
import random
import time
from enum import Enum
import threading

class StatusStudent(Enum):
    QUEUE = "Очередь"
    PASSED = "Сдал"
    FAILED = "Провалил"

class ExaminerMood(Enum):
    BAD = 0
    GOOD = 1
    NORMAL = 2
    
class Screen():
    def __init__(self, max_len_name_student, max_len_name_examiner, count_students, count_examiners):
        self.__screen = curses.initscr()
        self.__count_students = count_students
        self.__count_examiner = count_examiners
        if max_len_name_student > 7:
            self.__max_len_name_student = max_len_name_student
        else:
            self.__max_len_name_student = 7
        if max_len_name_examiner > 11:
            self.__max_len_name_examiner = max_len_name_examiner
        else:
            self.__max_len_name_examiner = 11
        if max_len_name_student > 15:
            self.__max_len_current_student = max_len_name_student
        else:
            self.__max_len_current_student = 15
    
    def draw_frame_table_student(self):
        horizontal_line = "+" + "-" * (2 + self.__max_len_name_student) + "+" + "-" * 10 + "+"
        headers_line = "| " + "Студент" + " " * (self.__max_len_name_student - 7) + " |  Статус  |"
        self.__screen.addstr(0, 0, horizontal_line)
        self.__screen.addstr(1, 0, headers_line)
        self.__screen.addstr(2, 0, horizontal_line)
        for i in range(self.__count_students):
            self.__screen.addstr(3 + i, 0, "|")
            self.__screen.addstr(3 + i, 1 + (2 + self.__max_len_name_student), "|")
            self.__screen.addstr(3 + i, 12 + (2 + self.__max_len_name_student), "|")
        self.__screen.addstr(3 + self.__count_students, 0, horizontal_line)
        
    def draw_frame_table_examiner(self, need_write_current_student):
        horizontal_line = ""
        headers_line = ""
        if need_write_current_student:
            horizontal_line = "+" + "-" * (2 + self.__max_len_name_examiner) + "+" + "-" * (2 + self.__max_len_current_student) + "+" + "-" * 17 + "+" + "-" * 9 + "+" + "-" * 14 + "+"
            headers_line = "| " + "Экзаменатор" + " " * (self.__max_len_name_examiner - 11) + " | Текущий студент" + " " * (self.__max_len_current_student - 15) + " | Всего студентов | Завалил | Время работы |"
        else:
            horizontal_line = "+" + "-" * (2 + self.__max_len_name_examiner) + "+" + "-" * 17 + "+" + "-" * 9 + "+" + "-" * 14 + "+"
            headers_line = "| " + "Экзаменатор" + " " * (self.__max_len_name_examiner - 11) + " | Всего студентов | Завалил | Время работы |"
        start_line_table = 5 + self.__count_students
        self.__screen.addstr(start_line_table, 0, horizontal_line)
        self.__screen.addstr(start_line_table + 1, 0, headers_line)
        self.__screen.addstr(start_line_table + 2, 0, horizontal_line)
        for i in range(self.__count_examiner):
            index_column = 0
            self.__screen.addstr(start_line_table + 3 + i, 0, "|")
            index_column += 1 + (2 + self.__max_len_name_examiner)
            self.__screen.addstr(start_line_table + 3 + i, index_column, "|")
            if need_write_current_student:
                index_column += 1 + (2 + self.__max_len_current_student)
                self.__screen.addstr(start_line_table + 3 + i, index_column, "|")
            index_column += 1 + 17
            self.__screen.addstr(start_line_table + 3 + i, index_column, "|")
            index_column += 1 + 9
            self.__screen.addstr(start_line_table + 3 + i, index_column, "|")
            index_column += 1 + 14
            self.__screen.addstr(start_line_table + 3 + i, index_column, "|")
        self.__screen.addstr(start_line_table + 3 + self.__count_examiner, 0, horizontal_line)
        
    def draw_table_frames(self, need_write_current_student):
        self.draw_frame_table_student()
        self.draw_frame_table_examiner(need_write_current_student)
        self.__screen.refresh()
    
    def close_screen(self):
        curses.endwin()
        
    def clear_screen(self):
        self.__screen.clear()
        self.__screen.refresh()
        
    def print_student_info(self, student_info, index_line):
        self.__screen.addstr(3 + index_line, 2, student_info[0] + " " * (self.__max_len_name_student - len(student_info[0])))
        self.__screen.addstr(3 + index_line, 3 + (2 + self.__max_len_name_student), student_info[1] + " " * (9 - len(student_info[1])))
        self.__screen.refresh()
    
    def print_examiner_info(self, examiner_info, index_line, need_write_current_student):
        line_table = 8 + self.__count_students
        index_column = 2
        self.__screen.addstr(line_table + index_line, index_column, examiner_info[0])
        index_column += 1 + (2 + self.__max_len_name_examiner)
        if need_write_current_student:
            self.__screen.addstr(line_table + index_line, index_column, examiner_info[1] + " " * (self.__max_len_current_student - len(examiner_info[1])))
            index_column += 1 + (2 + self.__max_len_current_student)
        self.__screen.addstr(line_table + index_line, index_column, str(examiner_info[2]))
        index_column += 1 + 17
        self.__screen.addstr(line_table + index_line, index_column, str(examiner_info[3]))
        index_column += 1 + 9
        self.__screen.addstr(line_table + index_line, index_column, str(examiner_info[4]))
        
        self.__screen.refresh()
    
    def print_status_exam(self, count_rest_students, time_start_exam):
        line_table = 10 + self.__count_students + self.__count_examiner
        rest_info = "Осталось в очереди: " + "{: ^3}".format(str(count_rest_students)) + " из " + str(self.__count_students)
        current_time = time.time()
        time_info = "Время с момента начала экзамена: " + "{:.2f}".format(current_time - time_start_exam)
        
        self.__screen.addstr(line_table, 0, rest_info)
        self.__screen.addstr(line_table + 1, 0, time_info)
        
        self.__screen.refresh()
        
    def print_final_info(self, info):
        line_table = 10 + self.__count_students + self.__count_examiner
        
        self.__screen.addstr(line_table, 0, "Время с момента начала экзамена и до момента и его завершения: " + info[0])
        self.__screen.addstr(line_table + 1, 0, "Имена лучших студентов: " + ", ".join(info[1]))
        self.__screen.addstr(line_table + 2, 0, "Имена лучших экзаменаторов: " + ", ".join(info[2]))
        self.__screen.addstr(line_table + 3, 0, "Имена студентов, которых после экзамена отчислят: " + ", ".join(info[3]))
        self.__screen.addstr(line_table + 4, 0, "Лучшие вопросы: " + ", ".join(info[4]))
        self.__screen.addstr(line_table + 5, 0, info[5])
        
        self.__screen.refresh()
        self.__screen.getch()
        
        
class Question():
    def __init__(self, text_question):
        self.text = text_question
        self.count_succes = 0
        self.count_failed = 0

class Human():
    def __init__(self, new_name, new_gender):
        if type(new_name) != str:
            raise ValueError("Некорректное имя")
        if new_gender != "М" and new_gender != "Ж":
            raise ValueError("Некорректный пол")
        self.__name = new_name
        self.__gender = new_gender

    @property
    def name(self):
        return str(self.__name)

    @property
    def gender(self):
        return self.__gender


class Student(Human):
    def __init__(self, new_name: str, new_gender: str, index: int):
        super().__init__(new_name, new_gender)
        self.status = StatusStudent("Очередь")
        self.time_exam = 0.0
        self.index = index
        self.need_sort = False
        
    def print_student(self, screen):
        info = [self.name, self.status.value]
        screen.print_student_info(info, self.index)

    def get_response_probabilities(self, number_responses: int):
        denominator = 0
        if number_responses % 2 == 0:
            denominator = (number_responses + 1) * (number_responses / 2)
        else:
            denominator = (number_responses + 1) * (number_responses // 2) + (number_responses + 1) / 2

        start_numerator = 1
        end_numerator = number_responses + 1
        increment = 1
        if self.gender == "М":
            start_numerator = number_responses
            end_numerator = 0
            increment = -1

        result = []
        sum_probabilities = 0.0

        for i in range(start_numerator, end_numerator, increment):
            sum_probabilities += i * 1.0 / denominator
            result.append(sum_probabilities)
        result[-1] = 1.0
        
        return result

    def get_answer(self, question: str):
        number_responses = len(question.split())
        response_probabilities = self.get_response_probabilities(number_responses)
        answer = 0
        random_value = random.random()
        for probability in response_probabilities:
            if random_value > probability:
                answer += 1
        return answer
    
    def change_index(self, new_index, screen):
        self.index = new_index
        self.print_student(screen)
    






class Examiner(Human):
    def __init__(self, new_name: str, new_gender: str, new_questions: list, index: int, list_students):
        if isinstance(new_questions, list) == False or len(new_questions) < 3:
            raise ValueError("Некорректный список вопросов")
        super().__init__(new_name, new_gender)
        self.__had_lunch = False
        self.on_lunch = False
        self.questions = new_questions
        
        mood_probabilities = [0.125, 0.375, 1]
        index_mood = 0
        random_value = random.random()
        for probability in mood_probabilities:
            if random_value > probability:
                index_mood += 1
        self.__mood = ExaminerMood(index_mood)

        self.current_student = None
        self.number_students = 0
        self.number_failed_students = 0
        self.time_work = 0.0
        self.index = index
        self.list_students = list_students
        
    def print_examiner(self, screen, need_write_current_student):
        str_for_current_student = "-"
        if self.current_student != None:
            str_for_current_student = self.current_student
        info = [self.name, str_for_current_student, str(self.number_students), str(self.number_failed_students), "{:.2f}".format(self.time_work)]
        screen.print_examiner_info(info, self.index, need_write_current_student)
    
    def lunch(self):
        self.on_lunch = True
        self.__had_lunch = True
        time_sleep = random.randint(12, 18)
        time.sleep(time_sleep)
        self.on_lunch = False

    def get_three_questions(self):
        result = set()
        while len(result) < 3:
            result.add(random.randint(0, len(self.questions) - 1))
        return result
    
    def get_current_answers(self, question: str):
        result = set()
        count_answers = len(question.split())
        max_index_answer = count_answers - 1
        result.add(random.randint(0, max_index_answer))
        selection_is_over = False
        while len(result) < count_answers and selection_is_over == False:
            if random.random() < 1/3:
                old_len_result = len(result)
                while len(result) == old_len_result:
                    result.add(random.randint(0, max_index_answer))
            else:
                selection_is_over = True
        return result
    
    def get_time_exam(self):
        len_name = len(self.name)
        result = random.uniform(len_name - 1, len_name + 1)
        return result
        
        
        
        
    def get_student(self, some_student: Student, screen):
        self.current_student = some_student.name
        self.number_students += 1
        self.print_examiner(screen, True)
        
    def exam(self, some_student: Student, screen):
        three_questions = self.get_three_questions()
        count_current_answers_student = 0
        count_wrong_answers_student = 0
        for question in three_questions:
            current_answers = self.get_current_answers(self.questions[question].text)
            answer_student = some_student.get_answer(self.questions[question].text)
            if answer_student in current_answers:
                count_current_answers_student += 1
                self.questions[question].count_succes += 1
            else:
                count_wrong_answers_student += 1
                self.questions[question].count_failed += 1
            
        result_exam = StatusStudent.QUEUE
        if self.__mood == ExaminerMood.BAD:
            result_exam = StatusStudent.FAILED
            self.number_failed_students += 1
        elif self.__mood == ExaminerMood.GOOD:
            result_exam = StatusStudent.PASSED
        elif count_current_answers_student > count_wrong_answers_student:
            result_exam = StatusStudent.PASSED
        else:
            result_exam = StatusStudent.FAILED
            self.number_failed_students += 1
        
        return result_exam
    
    def conduct_exam(self, some_student: Student, screen):
        self.get_student(some_student, screen)
        
        rest_time = self.get_time_exam()
        start_exam = time.time()
        result_exam = self.exam(some_student, screen)
        
        end_exam = time.time()
        rest_time = rest_time - (end_exam - start_exam)
        if rest_time > 0.0:
            time.sleep(rest_time)
            
        some_student.status = result_exam
        end_exam = time.time()
        self.time_work += (end_exam - start_exam)
        some_student.time_exam += (end_exam - start_exam)
        self.current_student = None
        some_student.need_sort = True
        self.print_examiner(screen, True)
        
        if self.time_work > 30.0 and self.__had_lunch == False:
            self.lunch()

    



def load_questions_students_examiners_screen():
    with open("questions.txt", "r") as file:
        questions_info = file.readlines()
    with open("students.txt", "r") as file:
        students_info = file.readlines()
    with open("examiners.txt", "r") as file:
        examiners_info = file.readlines()
    
    questions = []
    for question in questions_info:
        questions.append(Question(question))
    
    students = []
    index = 0
    max_len_name_student = 0
    for student in students_info:
        name, gender = student.split()
        students.append(Student(name, gender, index))
        if len(name) > max_len_name_student:
            max_len_name_student = len(name)
        index += 1
        
    examiners = []
    index = 0
    max_len_name_examiner = 0
    for examiner in examiners_info:
        name, gender = examiner.split()
        examiners.append(Examiner(name, gender, questions, index, students))
        if len(name) > max_len_name_examiner:
            max_len_name_examiner = len(name)
        index += 1
        
    new_screen = Screen(max_len_name_student, max_len_name_examiner, len(students_info), len(examiners_info))
    new_screen.draw_table_frames(True)
    
    return questions, students, examiners, new_screen
    
def print_current_info_exam(my_screen, students, examiners, time_start_exam):
    for student in students:
        student.print_student(my_screen)
    for examiner in examiners:
        examiner.print_examiner(my_screen, True)
    my_screen.print_status_exam(len(students), time_start_exam)

def sort_students(students, my_screen):
    index_student = 0
    need_write_table = False
    while index_student < len(students):
        if students[index_student].need_sort == True:
            need_write_table = True
            students[index_student].need_sort = False
            if students[index_student].status == StatusStudent.FAILED:
                student_for_replace = students.pop(index_student)
                students.append(student_for_replace)
            elif students[index_student].status == StatusStudent.PASSED:
                i = len(students) - 1
                while students[i].status == StatusStudent.FAILED and i > 0:
                    i -= 1
                student_for_replace = students.pop(index_student)
                students.insert(i, student_for_replace)
        else:
            index_student += 1
    
    if need_write_table:
        for i in range(len(students)):
            info = [students[i].name, students[i].status.value]
            my_screen.print_student_info(info, i)

def get_passed_failed_students(students):
    passed_students = []
    failed_students = []
    for student in students:
        if student.status == StatusStudent.PASSED:
            passed_students.append(student)
        elif student.status == StatusStudent.FAILED:
            failed_students.append(student)
    
    return passed_students, failed_students

def find_fasters_students(students):
    result = []
    min_time = -1.0
    for student in students:
        if student.time_exam == min_time:
            result.append(student.name)
        elif (min_time < 0 or student.time_exam < min_time):
            min_time = student.time_exam
            result.clear()
            result.append(student.name)
    return result

def find_best_examiners(examiners):
    result = []
    min_percentage = examiners[0].number_failed_students / examiners[0].number_students 
    for examiner in examiners:
        current_percentage = examiner.number_failed_students / examiner.number_students
        if current_percentage == min_percentage:
            result.append(examiner.name)
        elif current_percentage < min_percentage:
            min_percentage = current_percentage
            result.clear()
            result.append(examiner.name)
    return result
    
def find_best_questions(questions):
    result = []
    max_current_answers = 0
    for question in questions:
        if question.count_succes == max_current_answers:
            result.append(question.text)
        elif question.count_succes > max_current_answers:
            max_current_answers = question.count_succes
            result.clear()
            result.append(question.text)
    return result
    
def get_exam_status(count_passed_students, count_students):
    percentage_passers = (count_passed_students / count_students) * 100.0
    result = ""
    if percentage_passers > 85.0:
        result = "Вывод: экзамен удался                            "
    else:
        result = "Вывод: экзамен не удался                            "
    return result

def print_final_statistic(my_screen, questions, students, examiners, time_start_exam):
    time_end_exam = time.time()
    my_screen.clear_screen()
    my_screen.draw_table_frames(True)
    for i in range(len(students)):
        info = [students[i].name, students[i].status.value]
        my_screen.print_student_info(info, i)
    for examiner in examiners:
        examiner.print_examiner(my_screen, True)
        
    passed_students, failed_students = get_passed_failed_students(students)
    
    time_exam = "{:.2f}".format(time_end_exam - time_start_exam)
    best_students = find_fasters_students(passed_students)
    best_examiners = find_best_examiners(examiners)
    students_expulsion = find_fasters_students(failed_students)
    best_questions = find_best_questions(questions)
    exam_status = get_exam_status(len(passed_students), len(students))
    my_screen.print_final_info([time_exam, best_students, best_examiners, students_expulsion, best_questions, exam_status])

def main():  
    questions, students, examiners, my_screen = load_questions_students_examiners_screen()
    
    time_start_exam = time.time()
    print_current_info_exam(my_screen, students, examiners, time_start_exam)
    
    number_students_queue = len(students)
    index_next_student = 0
    queue_student = students.copy()
    while number_students_queue > 0:
        
        free_examiner = None
        for examiner in examiners:
            if free_examiner == None and examiner.current_student == None and examiner.on_lunch == False:
                free_examiner = examiner
        if free_examiner != None and index_next_student < len(students) and index_next_student > -1:
            t = threading.Thread(target=free_examiner.conduct_exam, args=(queue_student[index_next_student], my_screen, ))
            t.start()
            index_next_student += 1
        
        sort_students(students, my_screen)
        number_students_queue = 0
        for student in students:
            if student.status == StatusStudent.QUEUE:
                number_students_queue += 1
        my_screen.print_status_exam(number_students_queue, time_start_exam)
    sort_students(students, my_screen)
    print_final_statistic(my_screen, questions, students, examiners, time_start_exam)
    my_screen.close_screen()

if __name__ == "__main__":
    main()