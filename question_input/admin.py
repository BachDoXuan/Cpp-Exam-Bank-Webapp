from django.contrib import admin

# Register your models here.
from .models import CppQuestion, CppQuestionBase, EasyPracticeCppQuestion, EasyTheoryCppQuestion
from .models import MediumPracticeCppQuestion, MediumTheoryCppQuestion
from .models import HardPracticeCppQuestion, HardTheoryCppQuestion

admin.site.register(CppQuestion)
admin.site.register(EasyPracticeCppQuestion)
admin.site.register(EasyTheoryCppQuestion)
admin.site.register(MediumPracticeCppQuestion)
admin.site.register(MediumTheoryCppQuestion)
admin.site.register(HardPracticeCppQuestion)
admin.site.register(HardTheoryCppQuestion)
