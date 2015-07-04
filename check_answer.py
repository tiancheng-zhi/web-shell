import re

# class CheckAnswer is used to check whether the answer is correct

class CheckAnswer:

	# question number
	__question_num = -1

	def __init__(self, question_num):
		self.__question_num = question_num
		self.__stat = 0

	# check the answer of question 0
	def __check_func0(self, input_cmd, output_rst):
		if (output_rst == '"Hello World!"'):
			return True
		else:
			return False

	# check the answer of question 1
	def __check_func1(self, input_cmd, output_rst):
		r = re.compile(r'^\s*./my.sh\s+apple\s+pear\s+peach\s*$')
		if (r.match(input_cmd) and output_rst == 'pears'):
			return True
		else:
			return False

	# check the answer of question 2
	def __check_func2(self, input_cmd, output_rst):
		r = re.compile(r'^\s*./month.sh\s+2004\s+2\s*$')
		if (r.match(input_cmd) and output_rst == '29'):
			return True
		else:
			return False

	# check the answer of question 3
	def __check_func3(self, input_cmd, output_rst):
		r = re.compile(r'^\s*./printeven.sh\s+15\s*$')
		if (r.match(input_cmd) and output_rst == '0\n2\n4\n6\n8\n10\n12\n14'):
			return True
		else:
			return False

	# check the answer of question 4
	def __check_func4(self, input_cmd, output_rst):
		r = re.compile(r'^\s*./tom.sh\s+Tom\s+Black\s*$')
		if (r.match(input_cmd) and output_rst == 'OK'):
			return True
		else:
			return False

	# check the answer of question 5
	def __check_func5(self, input_cmd, output_rst):
		r = re.compile(r'^\s*./year.sh\s+1900\s*$')
		if (r.match(input_cmd) and output_rst == 'NO'):
			return True
		else:
			return False

	# check the answer of question 6
	def __check_func6(self, input_cmd, output_rst):
		r = re.compile(r'^\s*ls\s+\-l\s+|\s+sort\s+\-k\s*5\s+>\s*fileinfo\.txt\s*$')
		if (r.match(input_cmd)):
			return True
		else:
			return False

	# fucntion dictionary
	__check_func = {
					-1:None,
					0: __check_func0,
					1: __check_func1,
					2: __check_func2,
					3: __check_func3,
					4: __check_func4,
					5: __check_func5,
					6: __check_func6
					}

	# check answer
	def check_ans(self, input_cmd, output_rst):
		return self.__check_func.get(self.__question_num)(self, input_cmd, output_rst.strip())

