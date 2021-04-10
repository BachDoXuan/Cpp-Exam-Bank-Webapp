from django.shortcuts import render

# Create your views here.
from .models import CppQuestion, EasyPracticeCppQuestion, EasyTheoryCppQuestion, MediumPracticeCppQuestion, MediumTheoryCppQuestion, HardPracticeCppQuestion, HardTheoryCppQuestion
from .forms import CppQuestionForm


def input_question(request):
    if request.method == 'POST':
        # create a form instance and populate it with the request's data
        # to validate the request's data and transform them to a cleaned format
        question_form = CppQuestionForm(request.POST)
        if question_form.is_valid():
            cleaned_form = question_form.cleaned_data

            if (cleaned_form["question_type"] == "TH") and (cleaned_form["question_level"] == "E"):
                question = EasyTheoryCppQuestion(
                    question_content=cleaned_form["question_content"],
                    question_answer=cleaned_form["question_answer"]
                )
            elif (cleaned_form["question_type"] == "TH") and (cleaned_form["question_level"] == "M"):
                question = MediumTheoryCppQuestion(
                    question_content=cleaned_form["question_content"],
                    question_answer=cleaned_form["question_answer"]
                )
            elif (cleaned_form["question_type"] == "TH") and (cleaned_form["question_level"] == "H"):
                question = HardTheoryCppQuestion(
                    question_content=cleaned_form["question_content"],
                    question_answer=cleaned_form["question_answer"]
                )
            elif (cleaned_form["question_type"] == "PR") and (cleaned_form["question_level"] == "E"):
                question = EasyPracticeCppQuestion(
                    question_content=cleaned_form["question_content"],
                    question_answer=cleaned_form["question_answer"]
                )
            elif (cleaned_form["question_type"] == "PR") and (cleaned_form["question_level"] == "M"):
                question = MediumPracticeCppQuestion(
                    question_content=cleaned_form["question_content"],
                    question_answer=cleaned_form["question_answer"]
                )
            elif (cleaned_form["question_type"] == "PR") and (cleaned_form["question_level"] == "H"):
                question = HardPracticeCppQuestion(
                    question_content=cleaned_form["question_content"],
                    question_answer=cleaned_form["question_answer"]
                )

            # save inputted question to database
            question.save()

            return render(request, 'input_question_result.html', {'is_success': True})

    question_form = CppQuestionForm()
    return render(request, "input_question.html", {'question_form': question_form})
