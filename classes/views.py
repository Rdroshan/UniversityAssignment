from rest_framework.decorators import api_view
from rest_framework.response import Response

#import services
from .services import ClassService
from students.services import StudentService

@api_view(http_method_names=['GET'])
def get_all_classes(request):
	response = ClassService.get_all_classes()
	return Response(response)


@api_view(http_method_names=['GET'])
def get_class_students(request, pk):
	"""
	Gets all the students attended this class
	"""

	return


@api_view(http_method_names=['GET'])
def get_class_performance(request, pk):
	"""
	
	"""
	return


@api_view(http_method_names=['GET'])
def get_final_grade_sheet(request, pk):
	"""
	Grade sheet of students for a class
	"""

	return


@api_view(http_method_names=['GET'])
def get_student_class_details(request, class_id, student_id):
	"""
	Get marks obtained by a student in a particular class
	"""
	class_id = int(class_id)
	student_id = int(student_id)
	student_service = StudentService(student_id=student_id)
	student_name = student_service.get_student()
	
	response = student_service.get_student_class_details(class_id=class_id, student_name=student_name[0]['name'])

	return Response(response)