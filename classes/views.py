from rest_framework.decorators import api_view


@api_view(http_method_names=['GET'])
def get_all_classes(request):
	
	return

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

	return