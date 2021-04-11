import csv

from question_input.models import CppQuestion, EasyPracticeCppQuestion, EasyTheoryCppQuestion, MediumPracticeCppQuestion, MediumTheoryCppQuestion, HardPracticeCppQuestion, HardTheoryCppQuestion

def handle_uploaded_csv_file(f):
    """
    """
    with open('question_input/uploaded/csv_questions.csv', 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    with open('question_input/uploaded/csv_questions.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # print(', '.join(row))
            if (row[0] == "Theory") and (row[1] == "Easy"):
                question = EasyTheoryCppQuestion(
                    question_content=row[2],
                    question_answer=row[3]
                )
            elif (row[0] == "Theory") and (row[1] == "Medium"):
                question = MediumTheoryCppQuestion(
                    question_content=row[2],
                    question_answer=row[3]
                )
            elif (row[0] == "Theory") and (row[1] == "Hard"):
                question = HardTheoryCppQuestion(
                    question_content=row[2],
                    question_answer=row[3]
                )
            elif (row[0] == "Practice") and (row[1] == "Easy"):
                question = EasyPracticeCppQuestion(
                    question_content=row[2],
                    question_answer=row[3]
                )
            elif (row[0] == "Practice") and (row[1] == "Medium"):
                question = MediumPracticeCppQuestion(
                    question_content=row[2],
                    question_answer=row[3]
                )
            elif (row[0] == "Practice") and (row[1]== "Hard"):
                question = HardPracticeCppQuestion(
                    question_content=row[2],
                    question_answer=row[3]
                )
            question.save()