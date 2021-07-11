from clients import db


class StudentService:
	def __init__(self, student_id):
		self.student_id = student_id

	@staticmethod
	def get_all_students():
		"""
		This service will return all the present students
		:return:
			[
				{
					"student_id": int,
					"student_name": str
				}
			]
		"""
		students_data = db['students'].find({})
		response = []
		for student_data in students_data:
			response.append({"student_id": student_data['_id'], "student_name": student_data['name']})
		return response

	@staticmethod
	def map_class_marks_of_student(student_class_data):

		"""
		This service maps the class id with the marks and total_marks for a particular student
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
			<class_id>: {
				"marks": [
					"type": str,
					"marks": float
				],
				"total_marks": float
			}
		}
		"""
		# Creating a map to store the class(if duplicates then consider the class with highest aggregate sum of scores)
		student_classes = {}
		for class_data in student_class_data:
			scores = class_data['scores']
			total_score = 0
			new_score_data = []
			for score in scores:
				total_score += score['score']
				new_score_data.append({
						"type": score['type'],
						"marks": score['score']
					})
			if student_classes.get('class_id', {}).get('total_marks', 0) < total_score:
				student_classes[class_data['class_id']] = {
					"marks": new_score_data,
					"total_marks": total_score
				}
		return student_classes

	def get_student(self):
		"""
		This service gets the student data
		:return:
			[
				{
					"_id": int,
					"name": str
				},
			]
		"""
		student_data = db['students'].find(filter={'_id': self.student_id})
		if student_data.count() == 0:
			raise ParseError(detail="No such student found", code="student_not_found")
		return list(student_data)

	def get_classes_attended(self, student_name):
		"""
		This service gets the classes detail of a student
		:param student_name: str
		:return:
			{
				"student_id": int,
				"student_name": str,
				"classes": [
					{"class_id": int},
				]
			}
		"""
		student_class_ids = db['grades'].distinct("class_id", {"student_id": self.student_id})
		student_data = {
			"student_id": self.student_id,
			"student_name": student_name,
			"classes": []
		}
		for student_class_id in student_class_ids:
			student_data['classes'].append({"class_id": student_class_id})
		return student_data

	def get_student_performance(self, student_name):
		"""
		:param student_name: str
		:return:
			{
				"student_id": int,
				"student_name": str,
				"classes":[
					{"class_id": int,"total_marks":float},
				]
			}
		"""
		student_class_data = db['grades'].find(filter={"student_id": self.student_id})
		student_data = {
			"student_id": self.student_id,
			"student_name": student_name,
			"classes": []
		}

		student_classes = self.map_class_marks_of_student(student_class_data=list(student_class_data))

		for student_class_id in student_classes.keys():
			student_data['classes'].append({
					"class_id": student_class_id,
					"total_marks": student_classes[student_class_id]['total_marks']
				})
		return student_data

	def get_student_class_details(self, class_id, student_name):
		"""
		:param class_id: int
		:param student_name: str
		:return:
			{
				"student_id": int,
				"student_name": str,
				"class_id": int,
				"marks":[
					{"type": str,"marks":float},
				]
			}
		"""
		student_data = {
			"student_id": self.student_id,
			"student_name": student_name,
			"class_id": class_id,
			"marks": []
		}

		student_class_data = db['grades'].find(filter={"student_id": self.student_id, "class_id": class_id})
		student_classes = self.map_class_marks_of_student(student_class_data=list(student_class_data))

		for student_class_id in student_classes.keys():
			student_data['marks'].extend(student_classes[student_class_id]['marks'])

		return student_data



def func_Q1(db):
	return len(db['grades'].distinct("student_id"))

def func_Q2(db):
	return len(db['grades'].distinct("class_id"))