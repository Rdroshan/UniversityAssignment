from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from bson.json_util import dumps

# import clients
from clients import db


# import serializers
from .serializers import StudentSerializer

# import services
from .services import StudentService


@api_view(http_method_names=['GET'])
def get_all_students(request):
	response = StudentService.get_all_students()
	return Response(StudentSerializer(response, many=True).data)

@api_view(http_method_names=['GET'])
def get_student_classes(request, pk):
	"""
	Gets the classes a student had attended
	"""
	student_id = int(pk)
	student_service = StudentService(student_id)
	student_name = student_service.get_student()

	response = student_service.get_classes_attended(student_name=student_name[0]['name'])
	return	Response(response)


@api_view(http_method_names=['GET'])
def get_student_performance(request, pk):
	"""
	Gets performance for the student for each class
	"""
	student_id = int(pk)
	student_service = StudentService(student_id)
	student_name = student_service.get_student()


	response = student_service.get_student_performance(student_name=student_name[0]['name'])

	return	Response(response)


@api_view(http_method_names=['GET'])
def get_student_class_details(request, student_id, class_id):
	"""
	Get marks obtained by a student in a particular class
	"""
	student_id = int(student_id)
	class_id = int(class_id)

	student_service = StudentService(student_id=student_id)
	student_name = student_service.get_student()
	
	response = student_service.get_student_class_details(class_id=class_id, student_name=student_name[0]['name'])

	return Response(response)
