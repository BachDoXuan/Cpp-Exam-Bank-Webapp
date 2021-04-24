from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect

def index(request):
    return render(request, 'index.html', {
        "Can_generate_exams": request.user.is_authenticated and request.user.groups.filter(name="Can_generate_exams").exists(),
        "Can_download_all_questions": request.user.is_authenticated and request.user.groups.filter(name="Can_download_all_questions").exists(),
        "Can_input_exams": request.user.is_authenticated and request.user.groups.filter(name="Can_input_exams").exists(),
        "Can_upload_questions": request.user.is_authenticated and request.user.groups.filter(name="Can_upload_questions").exists(),
    })
