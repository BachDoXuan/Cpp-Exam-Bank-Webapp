# Create your views here.
from question_input.models import EasyPracticeCppQuestion, EasyTheoryCppQuestion, MediumPracticeCppQuestion, MediumTheoryCppQuestion, HardPracticeCppQuestion, HardTheoryCppQuestion

from django.http import FileResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.flowables import PageBreak, Spacer
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from .forms import ExamRequestForm
import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle
from reportlab.lib import colors
from zipfile import ZipFile
import random
import io
import logging
import os
import shutil

logging.basicConfig(filename='exam_generation/log/exam_generation.log',
                    encoding='utf-8', level=logging.DEBUG)

from .utils.utils import build_exam

def generate_exam(request):
    if request.method == 'POST':
        request_form = ExamRequestForm(request.POST)
        if not request_form.is_valid():
            return render(request, "generate_exam.html", {'request_form': request_form})

        num_exams = request_form.cleaned_data["num_exams"]

        base_name = "exam_generation/response/"
        # remove old files in base_name directory
        for file_name in os.listdir(base_name):
            file_path = os.path.join(base_name, file_name)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.critical(
                    'Failed to delete {}. Reason: {}'.format(file_path, e))

        zip_file_name = "exams.zip"
        zip_file = ZipFile(base_name + zip_file_name, 'w')
        for i in range(num_exams):
            file_name = "exam-" + str(i+1) + ".pdf"
            file_answer_name = "exam-" + str(i+1) + "-answer.pdf"
            build_exam(i, base_name + file_name, base_name + file_answer_name)
            zip_file.write(base_name + file_name, file_name)
            zip_file.write(base_name + file_answer_name, file_answer_name)

        zip_file.close()

        return FileResponse(open(base_name + zip_file_name, 'rb'), as_attachment=True, filename=zip_file_name)

    request_form = ExamRequestForm()
    return render(request, "generate_exam.html", {'request_form': request_form})
