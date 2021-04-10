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


############## report lab ########################

styleSheet = getSampleStyleSheet()
MARGIN_SIZE = 25 * mm
PAGE_SIZE = A4

width, height = letter

pdfmetrics.registerFont(TTFont('arialbd', 'exam_generation/data/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('arial', 'exam_generation/data/arial.ttf'))
black = colors.black


class PageNumCanvas(canvas.Canvas):
    """
    """
    # ----------------------------------------------------------------------

    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    # ----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()

    # ----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)

    # ----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """
        Add the page number
        """
        page = "Page %s of %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 9)
        self.drawRightString(195*mm, 272*mm, page)


def retrieve_exam():
    """
    Get exams from database
    """
    # 1 exam: theory - 2 easy, 2 medium, 1 hard ; practice - 2 easy, 2 medium, 1 hard
    easy_theory_count = EasyTheoryCppQuestion.objects.count()
    assert easy_theory_count >= 2, "Not enough easy theory questions"

    logging.debug(
        "Total number of easy theory questions: {}".format(easy_theory_count))
    th_q1_offset, th_q2_offset = random.sample(range(easy_theory_count), 2)
    th_q1 = EasyTheoryCppQuestion.objects.all()[th_q1_offset]
    th_q2 = EasyTheoryCppQuestion.objects.all()[th_q2_offset]

    medium_theory_count = MediumTheoryCppQuestion.objects.count()
    assert medium_theory_count >= 2, "Not enough medium theory questions"

    logging.debug("Total number of medium theory questions: {}".format(
        medium_theory_count))
    th_q3_offset, th_q4_offset = random.sample(
        range(medium_theory_count), 2)
    th_q3 = MediumTheoryCppQuestion.objects.all()[th_q3_offset]
    th_q4 = MediumTheoryCppQuestion.objects.all()[th_q4_offset]

    hard_theory_count = HardTheoryCppQuestion.objects.count()
    assert hard_theory_count >= 1, "Not enough hard theory questions"

    logging.debug(
        "Total number of hard theory questions: {}".format(hard_theory_count))
    th_q5 = HardTheoryCppQuestion.objects.all(
    )[random.randint(0, hard_theory_count-1)]

    easy_practice_count = EasyPracticeCppQuestion.objects.count()
    logging.debug("Total number of easy practice questions: {}".format(
        easy_practice_count))
    assert easy_practice_count >= 2, "Not enough easy practice questions"
    pr_q1_offset, pr_q2_offset = random.sample(
        range(easy_practice_count), 2)
    pr_q1 = EasyPracticeCppQuestion.objects.all()[pr_q1_offset]
    pr_q2 = EasyPracticeCppQuestion.objects.all()[pr_q2_offset]

    medium_practice_count = MediumPracticeCppQuestion.objects.count()
    logging.debug("Total number of medium practice questions: {}".format(
        medium_practice_count))
    assert medium_practice_count >= 2, "Not enough medium practice questions"
    pr_q3_offset, pr_q4_offset = random.sample(
        range(medium_practice_count), 2)
    pr_q3 = MediumPracticeCppQuestion.objects.all()[pr_q3_offset]
    pr_q4 = MediumPracticeCppQuestion.objects.all()[pr_q4_offset]

    hard_practice_count = HardPracticeCppQuestion.objects.count()
    logging.debug("Total number of hard practice questions: {}".format(
        hard_practice_count))
    assert hard_practice_count >= 1, "Not enough hard practice questions"
    pr_q5 = HardPracticeCppQuestion.objects.all(
    )[random.randint(0, hard_practice_count-1)]

    return th_q1, th_q2, th_q3, th_q4, th_q5, pr_q1, pr_q2, pr_q3, pr_q4, pr_q5


def add_page_number(canvas, doc):
    """
    Add the page number
    """
    page_num = canvas.getPageNumber()
    text = "Page #%s" % page_num
    canvas.drawRightString(200*mm, 20*mm, text)


BREAK = '<br />'

def create_pdfdoc(output, content):
    """
    Creates PDF doc from content.
    """
    pdf_doc = SimpleDocTemplate(output, pagesize=PAGE_SIZE,
                                leftMargin=MARGIN_SIZE, rightMargin=MARGIN_SIZE,
                                topMargin=MARGIN_SIZE, bottomMargin=MARGIN_SIZE)
    main_frame = Frame(MARGIN_SIZE, MARGIN_SIZE,
                       PAGE_SIZE[0] - 2 *
                       MARGIN_SIZE, PAGE_SIZE[1] - 2 * MARGIN_SIZE,
                       leftPadding=0, rightPadding=0, bottomPadding=0,
                       topPadding=0, id='main_frame')
    main_template = PageTemplate(id='main_template', frames=[main_frame])
    pdf_doc.addPageTemplates([main_template])

    pdf_doc.build(content, canvasmaker=PageNumCanvas)


def create_exam(idx, exam_tuple):
    """
    create exam from tuple of 10 questions
    """

    exam_content = []

    exam_content.append(Paragraph("C++ entry exam " + str(idx + 1), styleSheet['Title']))
    exam_content.append(Paragraph("Theory", styleSheet['Heading2']))
    for i in range(5):
        content = str(i+1) + ". " + exam_tuple[i].question_content
        content = content.replace('\n', BREAK)
        exam_content.append(Paragraph(content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))

    exam_content.append(PageBreak())
    exam_content.append(Paragraph("Practice", styleSheet['Heading2']))
    for i in range(5, 10):
        content = str(i+1) + ". " + exam_tuple[i].question_content
        content = content.replace('\n', BREAK)
        exam_content.append(Paragraph(content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))

    exam_content.append(PageBreak())

    return exam_content


def create_exam_answer(idx, exam_tuple):
    """
    create exam answer from exam tuple of 10 questions
    """
    exam_answer_content = []

    exam_answer_content.append(
        Paragraph("C++ entry exam " + str(idx + 1) + "'s answer", styleSheet['Title']))
    exam_answer_content.append(
        Paragraph("Theory answer", styleSheet['Heading2']))
    for i in range(5):
        content = (str(i+1) + ". " + exam_tuple[i].question_answer).replace('\n', BREAK)
        exam_answer_content.append(Paragraph(content, styleSheet['BodyText']))
        exam_answer_content.append(Spacer(0, 10 * mm))

    exam_answer_content.append(PageBreak())
    exam_answer_content.append(
        Paragraph("Practice answer", styleSheet['Heading2']))
    for i in range(5, 10):
        content = (str(i+1) + ". " + exam_tuple[i].question_answer).replace('\n', BREAK)
        exam_answer_content.append(Paragraph(content, styleSheet['BodyText']))
        exam_answer_content.append(Spacer(0, 10 * mm))

    return exam_answer_content


def build_exam(idx, exam_name, exam_answer_name):
    """
    Runs demo demonstrating usage of Spreadsheet Tables.
    """
    logging.debug('Generating C++ exam pdf file response to user...')

    # retrieve contents from database:
    exam_tuple = retrieve_exam()

    # create exam
    exam_content = create_exam(idx, exam_tuple)
    create_pdfdoc(exam_name, exam_content)

    # create exam answer content
    exam_answer_content = create_exam_answer(idx, exam_tuple)
    create_pdfdoc(exam_answer_name, exam_answer_content)


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
