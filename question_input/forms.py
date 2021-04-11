from django import forms


class CppQuestionForm(forms.Form):
    QUESTION_TYPES = [
        ('TH', 'Theory'),
        ('PR', 'Practice')
    ]
    question_type = forms.ChoiceField(
        label="Question type",
        choices=QUESTION_TYPES,
        widget=forms.RadioSelect,
        error_messages={
            'required': 'Need question type',
            'invalid_choice': 'Type %(value)s NOT exist.'
        }
    )

    QUESTION_LEVELS = [
        ('H', 'hard'),
        ('M', 'medium'),
        ('E', 'easy')
    ]
    question_level = forms.ChoiceField(
        label="Question level",
        choices=QUESTION_LEVELS,
        widget=forms.RadioSelect,
        error_messages={
            'required': 'Need question level',
            'invalid_choice': 'Level %(value)s NOT exist.'
        }
    )

    question_content = forms.CharField(
        label="Question content",
        max_length=1000,
        min_length=1,
        error_messages={
            'required': 'Need question content',
            'max_length': 'At most 1000 characters',
            'min_length': 'At least 1 characters'
        }
    )

    question_answer = forms.CharField(
        label="Question answer",
        max_length=1000,
        min_length=1,
        error_messages={
            'required': 'Need question answer',
            'max_length': 'At most 1000 characters',
            'min_length': 'At least 1 characters'
        }
    )


class CSVUploadFileForm(forms.Form):
    """
    to receive, validate, and clean uploaded csv file
    """
    csv_file = forms.FileField()