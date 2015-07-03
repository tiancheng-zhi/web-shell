import re

class CheckAnswer:

	__question_num = -1

	def __init__(self, question_num):
		self.__question_num = question_num
		self.__stat = 0

	def __check_func0(self, input_cmd, output_rst):
		r = re.compile(r'^\s*echo\s+\\"Hello World!\\"\s*$')
		if (r.match(input_cmd)):
			return True
		else:
			return False

	def __check_func1(self, input_cmd, output_rst):
		r = re.compile(r'^\s*./my.sh\s+apple\s+pear\s+peach\s*$')
		if (r.match(input_cmd) and output_rst == 'pears'):
			return True
		else:
			return False

	def __check_func2(self, input_cmd, output_rst):
		r = re.compile(r'^\s*./month.sh\s+2004\s+2\s*$')
		if (r.match(input_cmd) and output_rst == '29'):
			return True
		else:
			return False

	__check_func = {
					-1:None,
					0: __check_func0,
					1: __check_func1,
					2: __check_func2
					}

	def check_ans(self, input_cmd, output_rst):
		return self.__check_func.get(self.__question_num)(self, input_cmd, output_rst.strip())


