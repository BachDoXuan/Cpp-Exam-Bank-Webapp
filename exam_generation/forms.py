from django import forms

class ExamRequestForm(forms.Form):
    num_exams = forms.IntegerField(
        label="Number of exams to be generated",
        max_value=50,
        min_value=1,
        error_messages={
            'required': 'Need to provide a number from 1 to 50',
            'max_value': 'At most 50 exams',
            'min_value': 'At least 1 exam'
        }
    )

    choice = forms.CharField(
        max_length=50,
        min_length=1
    )

    previewed_exams = forms.CharField(
        
    )
