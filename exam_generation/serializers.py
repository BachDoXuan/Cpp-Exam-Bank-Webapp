from rest_framework import serializers

class Exam(object):
    def __init__(self, question_tuple):
        self.q1 = question_tuple[0].question_content
        self.q1_answer = question_tuple[0].question_answer
        self.q2 = question_tuple[1].question_content
        self.q2_answer = question_tuple[1].question_answer
        self.q3 = question_tuple[2].question_content
        self.q3_answer = question_tuple[2].question_answer
        self.q4 = question_tuple[3].question_content
        self.q4_answer = question_tuple[3].question_answer
        self.q5 = question_tuple[4].question_content
        self.q5_answer = question_tuple[4].question_answer
        self.q6 = question_tuple[5].question_content
        self.q6_answer = question_tuple[5].question_answer
        self.q7 = question_tuple[6].question_content
        self.q7_answer = question_tuple[6].question_answer
        self.q8 = question_tuple[7].question_content
        self.q8_answer = question_tuple[7].question_answer
        self.q9 = question_tuple[8].question_content
        self.q9_answer = question_tuple[8].question_answer
        self.q10 = question_tuple[9].question_content
        self.q10_answer = question_tuple[9].question_answer
class ExamSerializer(serializers.Serializer):
    q1 = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q1_answer = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q2 = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q2_answer = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q3 = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q3_answer = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q4 = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q4_answer = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q5 = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q5_answer = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q6 = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q6_answer = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q7 = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q7_answer = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q8 = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q8_answer = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q9 = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q9_answer = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q10 = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    q10_answer = serializers.CharField(required=False, allow_blank=True, max_length=1000)

