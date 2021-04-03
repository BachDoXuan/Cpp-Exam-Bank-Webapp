from django.shortcuts import render

# Create your views here.
from .models import CppQuestion
from .forms import CppQuestionForm

def input_question(request):
    if request.method == 'POST':
        # create a form instance and populate it with the request's data
        # to validate the request's data and transform them to a cleaned format
        question_form = CppQuestionForm(request.POST)
        if not question_form.is_valid():
            return render(request, 'input_question_result.html', {'is_success': False})
        
        cleaned_form = question_form.cleaned_data
        question = CppQuestion(
            question_type=cleaned_form["question_type"],
            question_level=cleaned_form["question_level"],
            question_content=cleaned_form["question_content"],
            question_answer=cleaned_form["question_answer"]
        )
        
        # save inputted question to database
        question.save()
        
        return render(request, 'input_question_result.html', {'is_success': True})
    else:
        question_form = CppQuestionForm()
        return render(request, "input_question.html", {'question_form': question_form})
