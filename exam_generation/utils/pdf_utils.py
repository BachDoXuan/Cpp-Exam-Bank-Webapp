# Create your views here.
from question_input.models import EasyPracticeCppQuestion, EasyTheoryCppQuestion, MediumPracticeCppQuestion, MediumTheoryCppQuestion, HardPracticeCppQuestion, HardTheoryCppQuestion

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.flowables import PageBreak, Spacer
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, SimpleDocTemplate, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

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
        text = "Page %s| %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 9)
        self.drawRightString(200*mm, 20*mm, text)

def retrieve_exam():
    """
    Get exams from database
    """
    # 1 exam: theory - 2 easy, 2 medium, 1 hard ; practice - 2 easy, 2 medium, 1 hard
    easy_theory_count = EasyTheoryCppQuestion.objects.count()
    assert easy_theory_count >= 2, "Not enough easy theory questions"

    logging.debug(
        "Total number of easy theory questions: {}".format(easy_theory_count))
    l = list(range(easy_theory_count))
    random.shuffle(l)
    th_q1_offset, th_q2_offset = l[0:2]
    th_q1 = EasyTheoryCppQuestion.objects.all()[th_q1_offset]
    th_q2 = EasyTheoryCppQuestion.objects.all()[th_q2_offset]

    medium_theory_count = MediumTheoryCppQuestion.objects.count()
    assert medium_theory_count >= 2, "Not enough medium theory questions"

    logging.debug("Total number of medium theory questions: {}".format(
        medium_theory_count))
    l = list(range(medium_theory_count))
    random.shuffle(l)
    th_q3_offset, th_q4_offset = l[0:2]
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
    l = list(range(easy_practice_count))
    random.shuffle(l)
    pr_q1_offset, pr_q2_offset = l[0:2]
    pr_q1 = EasyPracticeCppQuestion.objects.all()[pr_q1_offset]
    pr_q2 = EasyPracticeCppQuestion.objects.all()[pr_q2_offset]

    medium_practice_count = MediumPracticeCppQuestion.objects.count()
    logging.debug("Total number of medium practice questions: {}".format(
        medium_practice_count))
    assert medium_practice_count >= 2, "Not enough medium practice questions"
    l = list(range(medium_practice_count))
    random.shuffle(l)
    pr_q3_offset, pr_q4_offset = l[0:2]
    pr_q3 = MediumPracticeCppQuestion.objects.all()[pr_q3_offset]
    pr_q4 = MediumPracticeCppQuestion.objects.all()[pr_q4_offset]

    hard_practice_count = HardPracticeCppQuestion.objects.count()
    logging.debug("Total number of hard practice questions: {}".format(
        hard_practice_count))
    assert hard_practice_count >= 1, "Not enough hard practice questions"
    pr_q5 = HardPracticeCppQuestion.objects.all(
    )[random.randint(0, hard_practice_count-1)]

    return th_q1, th_q2, th_q3, th_q4, th_q5, pr_q1, pr_q2, pr_q3, pr_q4, pr_q5





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

    I = Image('exam_generation/static/images/LG logo.jpg')
    I.drawHeight = 2 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 2 * inch
    exam_content.append(I)
    exam_content.append(Spacer(0, 5 * mm))
    exam_content.append(Paragraph("<para align=center><b>ENTRANCE TEST FOR FRESHER SOFTWARE ENGINEER</b></para>", styleSheet['BodyText']))
    exam_content.append(Paragraph("<para align=center><b>Duration: 30 minutes</b></para>", styleSheet['BodyText']))
    exam_content.append(Spacer(0, 5 * mm))
    exam_content.append(Paragraph("<para align=left><b>Full name</b> .................................................</para>", styleSheet['BodyText']))
    exam_content.append(Paragraph("<para align=left><b>Date of Birth</b> ............................................</para>", styleSheet['BodyText']))
    exam_content.append(Paragraph("<para align=left><b>Score</b> ......../ <b>100</b>........................................</para>", styleSheet['BodyText']))
    exam_content.append(Spacer(0, 5 * mm))
    # exam_content.append(Paragraph("Theory", styleSheet['Heading2']))
    for i in range(5):
        content = "<b>Question " + str(i+1) + ". </b>" + exam_tuple[i].question_content
        content = content.replace('\n', BREAK)
        exam_content.append(Paragraph(content, styleSheet['BodyText']))
        exam_content.append(Spacer(0, 10 * mm))

    exam_content.append(PageBreak())
    # exam_content.append(Paragraph("Practice", styleSheet['Heading2']))
    for i in range(5, 10):
        content = "<b>Question " + str(i+1) + ". </b>" + exam_tuple[i].question_content
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
        content = ("<b>" + str(i+1) + ")</b>" + BREAK + exam_tuple[i].question_answer).replace('\n', BREAK)
        exam_answer_content.append(Paragraph(content, styleSheet['BodyText']))
        exam_answer_content.append(Spacer(0, 10 * mm))

    exam_answer_content.append(PageBreak())
    exam_answer_content.append(
        Paragraph("Practice answer", styleSheet['Heading2']))
    for i in range(5, 10):
        content = ("<b>" + str(i+1) + ")</b>" + BREAK + exam_tuple[i].question_answer).replace('\n', BREAK)
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