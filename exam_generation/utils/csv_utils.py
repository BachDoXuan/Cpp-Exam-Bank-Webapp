import csv

from question_input.models import CppQuestionBase, EasyPracticeCppQuestion, EasyTheoryCppQuestion, MediumPracticeCppQuestion, MediumTheoryCppQuestion, HardPracticeCppQuestion, HardTheoryCppQuestion

def generate_csv_backup(response):
    """
    """
    writer = csv.writer(response)

    for question in EasyTheoryCppQuestion.objects.all():
        writer.writerow(["Theory", "Easy", question.question_content, question.question_answer])

    for question in MediumTheoryCppQuestion.objects.all():
        writer.writerow(["Theory", "Medium", question.question_content, question.question_answer])

    for question in HardTheoryCppQuestion.objects.all():
        writer.writerow(["Theory", "Hard", question.question_content, question.question_answer])

    for question in EasyPracticeCppQuestion.objects.all():
        writer.writerow(["Practice", "Easy", question.question_content, question.question_answer])

    for question in MediumPracticeCppQuestion.objects.all():
        writer.writerow(["Practice", "Medium", question.question_content, question.question_answer])

    for question in HardPracticeCppQuestion.objects.all():
        writer.writerow(["Practice", "Hard", question.question_content, question.question_answer])
    