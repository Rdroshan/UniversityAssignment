from rest_framework.exceptions import ParseError

# import clients
from clients import db


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

	def get_class(self):
		class_data = db['grades'].find(filter={'class_id': self.class_id})
		if class_data.count() == 0:
			raise ParseError(detail="No such class found", code="class_not_found")
		return list(class_data)


	def get_class_data(self):
		"""
		This service gets the class and its student data
		:return:
			{
				"class_id": int,
				"students": [
					{
						"student_id": int,
						"student_name": str
					}
				]
			}
		"""
		class_data = self.get_class()