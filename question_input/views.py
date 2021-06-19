from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
from .models import EasyPracticeCppQuestion, EasyTheoryCppQuestion, MediumPracticeCppQuestion, MediumTheoryCppQuestion, HardPracticeCppQuestion, HardTheoryCppQuestion
from .forms import CppQuestionForm, CSVUploadFileForm

from .utils.csv_upload_utils import handle_uploaded_csv_file

@login_required
def input_question(request):
    if not request.user.groups.filter(name = 'Can_input_exams').exists():
        return redirect('index')

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

            return render(request, 'input_question.html', {"return_success": True})

    question_form = CppQuestionForm()
    return render(request, "input_question.html", {'question_form': question_form})

@login_required
def upload_csv(request):
    """
    """
    if not request.user.groups.filter(name = 'Can_input_exams').exists():
        return redirect('index')
        
    if request.method == 'POST':
        form = CSVUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_csv_file(request.FILES['csv_file'])
    else:
        form = CSVUploadFileForm()

    return render(request, "csv_upload.html", {'form': form})