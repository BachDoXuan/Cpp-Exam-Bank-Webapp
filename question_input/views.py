from django.shortcuts import render

# Create your views here.
def input_question(request):
    return render(request, "input_question.html")