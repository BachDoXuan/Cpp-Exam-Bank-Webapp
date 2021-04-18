from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect

def index(request):
    return render(request, 'index.html')
    # return redirect('signin')
    # return redirect('input_question')