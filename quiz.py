from random import shuffle
from operator import attrgetter

MAX_ANSWERS = 4

class Question:

    def __init__(self, question, answer):
        self.wrong_answers = []
        self.question = question
        self.answer = answer

    def add_wrong(self, wrong_ans):
        wrong_ans = WrongAnswer(wrong_ans)
        self.wrong_answers.append(wrong_ans)

    def ask(self):
        print(self.question)
        l_answers = []
        best_wrong_ans = sorted(self.wrong_answers, key=attrgetter('score'), reverse=True)
        l_answers.append(self.answer)

        for answer in best_wrong_ans:
            if MAX_ANSWERS > len(l_answers):
                l_answers.append(answer)

        shuffle(l_answers)
        sorted_ans = []

        for number, answer in enumerate(l_answers, start=1):
            if isinstance(answer, WrongAnswer):
                print(f'{number}: {answer.wrong_ans}')
                sorted_ans.append((number, answer))
                answer.shown += 1
                answer.count_score()
            elif answer == self.answer:
                print(f'{number}: {answer}')

        correct_number = l_answers.index(self.answer)
        user_prompt = int(input("What is your answer? "))

        if correct_number != user_prompt:
            for answer in sorted_ans:
                if answer[0] == user_prompt:
                    answer[1].chosen += 1
                    answer[1].count_score()

        return user_prompt, correct_number + 1

class IntQuestion(Question):

    def ask(self):
        print(self.question)
        prompt = int(input('Your answer: '))
        return prompt, self.answer

class Quiz:
    def __init__(self, name):
        self.name = name
        self.questions = []

    def add_question(self, q):
        self.q = q
        self.questions.append(self.q)

    def do(self):
        print(self.name)
        print('=' * len(self.name))
        counter = 0
        for question in self.questions:
            answers_tuple = question.ask()
            if answers_tuple[0] == answers_tuple[1]:
                print('Correct! You got this!')
                counter += 1
            else:
                print('Sorry, false!')
                print(f'The correct answer is {answers_tuple[1]}.')

        print(f'You answered {counter} out of {len(self.questions)} questions.')

        if counter == len(self.questions):
            return True

    def do_until_right(self):
        while not self.do():
            #self.do
            print('\n')


class WrongAnswer:
    def __init__(self, wrong_ans):
        self.wrong_ans = wrong_ans
        self.score = 1
        self.chosen = 0
        self.shown = 0

    def count_score(self):
        self.score = (2 * self.chosen + 1) / (self.shown + 1)


def create_quiz_from_file(filename):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            command, data = line.split(' ', 1)
            data = data.strip()
            if command == 'name':
                quiz = Quiz(data)
            elif command == 'q':
                text = data
                q_kind = 'string_q'
            elif command == 'iq':
                text = data
                q_kind = 'int_q'
            elif command == 'a':
                if q_kind == 'string_q':
                    question = Question(text, data)
                elif q_kind == 'int_q':
                    question = IntQuestion(text, int(data))
                quiz.add_question(question)
            elif command == 'w':
                question.add_wrong(data)
    return quiz


dquiz = create_quiz_from_file('disney.quiz')
dquiz.do_until_right()