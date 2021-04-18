"""cpp_exam_bank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.conf.urls import url
from django.conf.urls import include

# home app
from home import views as home_views
from account_management import views as acccount_management_views
from exam_generation import views as exam_generation_views

urlpatterns += [
    path('', home_views.index, name='index'),
]

# question input app
from question_input import views as question_input_views

urlpatterns += [
    path('input_question', question_input_views.input_question, name='input_question'),
    path('upload_csv', question_input_views.upload_csv, name='upload_csv')
]


# account management app
urlpatterns += [
    path('signin', acccount_management_views.signin, name='signin'),
    path('signup', acccount_management_views.signup, name='signup')
]

# exam generation app
urlpatterns += [
    path('generate_exam', exam_generation_views.generate_exam, name='generate_exam'),
    path('csv_backup', exam_generation_views.backup_to_csv, name='backup_to_csv')
]
