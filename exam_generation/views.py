# Create your views here.
from .utils.csv_utils import generate_csv_backup
from .utils.pdf_utils import build_exam, retrieve_exam, create_exam, create_pdfdoc, create_exam_answer
from django.http.response import JsonResponse

from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from .forms import ExamRequestForm

from zipfile import ZipFile
import logging
import os
import shutil
import json

logging.basicConfig(filename='exam_generation/log/exam_generation.log',
                    encoding='utf-8', level=logging.ERROR)


@login_required
def generate_exam(request):
    if not request.user.groups.filter(name='Can_generate_exams').exists():
        return redirect('index')
    if request.method == 'POST':
        # print(request.POST)
        request_form = ExamRequestForm(request.POST)
        if not request_form.is_valid():
            # print("Form not valid\n")
            return render(request, "generate_exam.html", {'request_form': request_form})

        num_exams = request_form.cleaned_data["num_exams"]
        choice = request_form.cleaned_data["choice"]

        if (choice == "download") or (choice == "download_preview"):
            if choice == "download_preview":
                preview_exams = json.loads(request_form.cleaned_data["previewed_exams"])
                num_exams = len(preview_exams)

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
                if (choice == "download"):
                    build_exam(i, base_name + file_name,
                            base_name + file_answer_name)
                else:
                    # create exam
                    exam_content = create_exam(i, preview_exams[i], is_tuple=False)
                    create_pdfdoc(base_name + file_name, exam_content)

                    # create exam answer content
                    exam_answer_content = create_exam_answer(i, preview_exams[i], is_tuple=False)
                    create_pdfdoc(base_name + file_answer_name, exam_answer_content)

                zip_file.write(base_name + file_name, file_name)
                zip_file.write(base_name + file_answer_name, file_answer_name)

            zip_file.close()

            return FileResponse(open(base_name + zip_file_name, 'rb'), as_attachment=True, filename=zip_file_name)

        if choice == "preview":
            exams = []
            for i in range(num_exams):
                tuple_10_question = retrieve_exam()
                # generate exams and send back to user
                exams.append({"q1": tuple_10_question[0].question_content,
                              "q1_answer": tuple_10_question[0].question_answer,
                              "q2": tuple_10_question[1].question_content,
                              "q2_answer": tuple_10_question[1].question_answer,
                              "q3": tuple_10_question[2].question_content,
                              "q3_answer": tuple_10_question[2].question_answer,
                              "q4": tuple_10_question[3].question_content,
                              "q4_answer": tuple_10_question[3].question_answer,
                              "q5": tuple_10_question[4].question_content,
                              "q5_answer": tuple_10_question[4].question_answer,
                              "q6": tuple_10_question[5].question_content,
                              "q6_answer": tuple_10_question[5].question_answer,
                              "q7": tuple_10_question[6].question_content,
                              "q7_answer": tuple_10_question[6].question_answer,
                              "q8": tuple_10_question[7].question_content,
                              "q8_answer": tuple_10_question[7].question_answer,
                              "q9": tuple_10_question[8].question_content,
                              "q9_answer": tuple_10_question[8].question_answer,
                              "q10": tuple_10_question[9].question_content,
                              "q10_answer": tuple_10_question[9].question_answer})

            # serializer = ExamSerializer(data=exams, many=True)
            # if serializer.is_valid():
                # return JsonResponse(serializer.data, status=201, safe=False)
            # return JsonResponse(serializer.errors, status=400, safe=False)
            return JsonResponse(exams, status=201, safe=False)

    request_form = ExamRequestForm()
    return render(request, "generate_exam.html", {'request_form': request_form})


@login_required
def backup_to_csv(request):
    """
    Back up all questions in database to csv file.
    """
    if not request.user.groups.filter(name='Can_download_all_questions').exists():
        return redirect('index')
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="questions.csv"'

    generate_csv_backup(response)

    return response
