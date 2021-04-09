# Create your views here.
import io
import logging

logging.basicConfig(filename='exam_generation/data/exam_generation.log',
                    encoding='utf-8', level=logging.DEBUG)

import random

############## report lab ########################
from reportlab.lib import colors
from reportlab.platypus.tables import TableStyle
from reportlab.platypus.tables import Table
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import reportlab.rl_config
from .forms import ExamRequestForm
import random
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.units import mm
from reportlab.platypus.flowables import PageBreak, Spacer
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas

styleSheet = getSampleStyleSheet()
MARGIN_SIZE = 25 * mm
PAGE_SIZE = A4

width, height = letter

pdfmetrics.registerFont(TTFont('arialbd', 'exam_generation/data/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('arial', 'exam_generation/data/arial.ttf'))
black = colors.black

######### django ##############################
from django.shortcuts import render
from django.http import FileResponse

############ database ##########################
from question_input.models import *
################################################

def create_pdfdoc(output, exam_content):
    """
    Creates PDF doc from exam_content.
    """
    pdf_doc = BaseDocTemplate(output, pagesize=PAGE_SIZE,
                              leftMargin=MARGIN_SIZE, rightMargin=MARGIN_SIZE,
                              topMargin=MARGIN_SIZE, bottomMargin=MARGIN_SIZE)
    main_frame = Frame(MARGIN_SIZE, MARGIN_SIZE,
                       PAGE_SIZE[0] - 2 *
                       MARGIN_SIZE, PAGE_SIZE[1] - 2 * MARGIN_SIZE,
                       leftPadding=0, rightPadding=0, bottomPadding=0,
                       topPadding=0, id='main_frame')
    main_template = PageTemplate(id='main_template', frames=[main_frame])
    pdf_doc.addPageTemplates([main_template])

    pdf_doc.build(exam_content)


def build_exam(output):
    """
    Runs demo demonstrating usage of Spreadsheet Tables.
    """
    logging.debug('Generating C++ exam pdf file response to user...')

    # 1 exam: theory - 2 easy, 2 medium, 1 hard ; practice - 2 easy, 2 medium, 1 hard
    # get 10 questions described above from database

    try:
        exam_content = []
        exam_content.append(Paragraph("C++ entry exam", styleSheet['Title']))

        exam_content.append(Paragraph("Theory", styleSheet['Heading2']))
        
        easy_theory_count = EasyTheoryCppQuestion.objects.count()
        assert easy_theory_count >= 2, "Not enough easy theory questions"

        logging.debug("Total number of easy theory questions: {}".format(easy_theory_count))
        th_q1_offset, th_q2_offset = random.sample(range(easy_theory_count), 2)
        th_q1 = EasyTheoryCppQuestion.objects.all()[th_q1_offset]
        th_q2 = EasyTheoryCppQuestion.objects.all()[th_q2_offset]

        medium_theory_count = MediumTheoryCppQuestion.objects.count()
        assert medium_theory_count >= 2, "Not enough medium theory questions"

        logging.debug("Total number of medium theory questions: {}".format(medium_theory_count))
        th_q3_offset, th_q4_offset = random.sample(range(easy_theory_count), 2)
        th_q3 = MediumTheoryCppQuestion.objects.all()[th_q3_offset]
        th_q4 = MediumTheoryCppQuestion.objects.all()[th_q4_offset]

        hard_theory_count = HardTheoryCppQuestion.objects.count()
        assert hard_theory_count >= 1, "Not enough hard theory questions"

        logging.debug("Total number of hard theory questions: {}".format(hard_theory_count))
        th_q5 = HardTheoryCppQuestion.objects.all()[random.randint(0, hard_theory_count-1)]

        exam_content.append(Paragraph("1. " + th_q1.question_content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))
        exam_content.append(Paragraph("2. " + th_q2.question_content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))
        exam_content.append(Paragraph("3. " + th_q3.question_content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))
        exam_content.append(Paragraph("4. " + th_q4.question_content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))
        exam_content.append(Paragraph("5. " + th_q5.question_content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))


        exam_content.append(PageBreak())
        exam_content.append(Paragraph("Practice", styleSheet['Heading2']))

        easy_practice_count = EasyPracticeCppQuestion.objects.count()
        logging.debug("Total number of easy practice questions: {}".format(easy_practice_count))
        assert easy_practice_count >= 2, "Not enough easy practice question" 
        pr_q1_offset, pr_q2_offset = random.sample(range(easy_practice_count), 2)
        pr_q1 = EasyPracticeCppQuestion.objects.all()[pr_q1_offset]
        pr_q2 = EasyPracticeCppQuestion.objects.all()[pr_q2_offset]

        medium_practice_count = MediumPracticeCppQuestion.objects.count()
        logging.debug("Total number of medium practice questions: {}".format(medium_practice_count))
        assert medium_practice_count >= 2, "Not enough medium practice question"
        pr_q3_offset, pr_q4_offset = random.sample(range(easy_practice_count), 2)
        pr_q3 = MediumPracticeCppQuestion.objects.all()[pr_q3_offset]
        pr_q4 = MediumPracticeCppQuestion.objects.all()[pr_q4_offset]

        hard_practice_count = HardPracticeCppQuestion.objects.count()
        logging.debug("Total number of hard practice questions: {}".format(hard_practice_count))
        assert hard_practice_count >= 1, "Not enough hard practice question"
        pr_q5 = HardPracticeCppQuestion.objects.all()[random.randint(0, hard_practice_count-1)]

        exam_content.append(Paragraph("6. " + pr_q1.question_content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))
        exam_content.append(Paragraph("7. " + pr_q2.question_content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))
        exam_content.append(Paragraph("8. " + pr_q3.question_content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))
        exam_content.append(Paragraph("9. " + pr_q4.question_content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))
        exam_content.append(Paragraph("10. " + pr_q5.question_content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))

        exam_content.append(PageBreak())

        # create_pdfdoc('exam_generation/data/spreadsheet_demo.pdf', exam_content)
        create_pdfdoc(output, exam_content)
        return True
    except AssertionError:
        logging.critical("AssertionError")
        return False
    except Exception as ex:
        logging.critical("Unexpected error: {}".format(type(ex)))
        return False



def generate_exam(request):
    if request.method == 'POST':
        request_form = ExamRequestForm(request.POST)
        if not request_form.is_valid():
            return render(request, "generate_exam.html", {'request_form': request_form})

        # easy start first: generate pdf for 1 exam:
        buffer = io.BytesIO()

        if (build_exam(buffer)):
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename="exam.pdf")
    
    request_form = ExamRequestForm()
    return render(request, "generate_exam.html", {'request_form': request_form})
