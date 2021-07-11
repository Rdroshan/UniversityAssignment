"""UniversityApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from students import views as student_views
from classes import views as class_views

urlpatterns = [
	# student apis
    path('students/', student_views.get_all_students, name='get_all_students'),
    path('student/<pk>/classes/', student_views.get_student_classes, name='get_student_classes'),
    path('student/<pk>/performance/', student_views.get_student_performance, name='get_student_performance'),
    path('student/<student_id>/class/<class_id>/', student_views.get_student_class_details, name='get_student_class_details'),
    # class apis
    path('classes/', class_views.get_all_classes, name='get_all_classes'),
    path('class/<pk>/students/', class_views.get_class_students, name='get_class_students'),
    path('class/<pk>/performance/', class_views.get_class_performance, name='get_class_performance'),
    path('class/<pk>/final-grade-sheet/', class_views.get_final_grade_sheet, name='get_final_grade_sheet'),
    path('class/<class_id>/student/<student_id>/', class_views.get_student_class_details, name='get_class_student_details')

]
