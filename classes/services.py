from rest_framework.exceptions import ParseError

# import clients
from clients import db

from students.services import StudentService


class ClassService():
	def __init__(self, class_id):
		self.class_id = class_id

	@staticmethod
	def get_all_classes():
		"""
		:return: 
		[
			{"class_id": int,}
		]
		"""

		classes_data = list(db['grades'].find(filter={}, projection={'class_id': 1, '_id': 0}).distinct('class_id'))

		return classes_data

	def __map_class_students(self, class_student_data):

		"""
		This service maps the student id with the marks and total_marks for a particular student
		:param student_class_data:	
		[			
			{
				"_id": str,
				"student_id": int,
				"class_id": int,
				"scores": [
					{"type": str, "score": float},
				]
			}
		]

		:return:
		{
			<student_id>: {
				"marks": [
					{
						"type": str,
						"marks": float
					}
				],
				"total_marks": float
			}
		}
		"""
		student_classes = {}
		for student_data in class_student_data:
			scores = student_data['scores']
			student_id = student_data['student_id']
			total_score = 0
			new_score_data = []
			for score in scores:
				total_score += score['score']
				new_score_data.append({
					"type": score['type'],
					"marks": score['score']
				})
			if student_classes.get(student_id, {}).get('total_marks', 0) < total_score:
				student_classes[student_id] = {
					"marks": new_score_data,
					"total_marks": total_score
				}
		return student_classes


	def get_class(self):
		class_data = db['grades'].find(filter={'class_id': self.class_id})
		if class_data.count() == 0:
			raise ParseError(detail="No such class found", code="class_not_found")
		return list(class_data)

	def get_class_data(self):
		"""
		This service gets the students detail for a class
		:return:
			{
				"class_id": int,
				"students": [
					{
						"student_id": int,
						"student_name": str
					},
				]
			}
		"""
		student_ids = db['grades'].distinct("student_id", {"class_id": self.class_id})
		student_data = {
			"class_id": self.class_id,
			"students": []
		}

		# Create a mapping between student ids from above and their names
		students_name_data = StudentService.filter_students(filter={"_id": {"$in": list(student_ids)}})
		students_name_dict = {}
		for student_name_data in students_name_data:
			students_name_dict[student_name_data['_id']] = student_name_data['name']

		for student_id in student_ids:
			student_data['students'].append({
					"student_id": student_id,
					"student_name": students_name_dict[student_id]
				})
		return student_data

	def get_class_performance(self):
		"""
		This service gets the class and its student data
		:return:
			{
				"class_id": int,
				"students": [
					{
						"student_id": int,
						"student_name": str
						"total_marks": int
					}
				]
			}
		"""
		class_student_data = self.get_class()
		class_data = {
			"class_id": self.class_id,
			"students": []
		}
		# Create mapping between student and their 
		student_classes_dict = self.__map_class_students(class_student_data=class_student_data)

		# Create a mapping between student ids from above and their names
		students_name_data = StudentService.filter_students(filter={"_id": {"$in": list(student_classes_dict.keys())}})
		students_name_dict = {}
		for student_data in students_name_data:
			students_name_dict[student_data['_id']] = student_data['name']

		for student_id in student_classes_dict:
			class_data['students'].append({
					"student_id": student_id,
					"student_name": students_name_dict[student_id],
					"total_marks": student_classes_dict[student_id]['total_marks']
				})
		return class_data

	def __get_grade(self, rank, total_students):
		first_grade_range = total_students // 12
		second_grade_range = first_grade_range + (total_students // 6)
		third_grade_range = second_grade_range + (total_students // 4)
		if 1 <= rank <= first_grade_range:
			return "A"
		elif (first_grade_range + 1) <= rank <= second_grade_range:
			return "B"
		elif (second_grade_range + 1) <= rank <= third_grade_range:
			return "C"
		else:
			return "D"

	def get_final_grades(self):
		"""
		This service gets the class and its student data
		:return:
			{
				"class_id": int,
				"students": [
					{
						"student_id": int,
						"student_name": str
						"total_marks": int
					}
				]
			}
		"""
		class_student_data = self.get_class()
		class_data = {
			"class_id": self.class_id,
			"students": []
		}
		# Create mapping between student and their details
		student_details_dict = self.__map_class_students(class_student_data=class_student_data)
		
		# self.get_graded_student_details(student_details=student_details_dict)
		new_student_details = {}
		sorted_data_on_marks = sorted(student_details_dict.items(), key=lambda item: item[1]['total_marks'], reverse=True)
		rank = 1
		print(len(sorted_data_on_marks))
		for student_id, details in sorted_data_on_marks:
			grade = self.__get_grade(rank=rank, total_students=len(sorted_data_on_marks))
			print(grade)
			new_student_details[student_id] = {
				"details": details['marks'],
				"grade": grade
			}
			rank += 1

		# Create a mapping between student ids from above and their names
		students_name_data = StudentService.filter_students(filter={"_id": {"$in": list(new_student_details.keys())}})
		students_name_dict = {}
		for student_data in students_name_data:
			students_name_dict[student_data['_id']] = student_data['name']

		for student_id in new_student_details:
			class_data['students'].append({
					"student_id": student_id,
					"student_name": students_name_dict[student_id],
					"details": new_student_details[student_id]['details'],
					"grade": new_student_details[student_id]['grade']
				})
		return class_data