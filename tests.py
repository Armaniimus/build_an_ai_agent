# tests.py

import unittest
from functions.get_files_info import get_files_info, get_file_content

class TestFilesInfo(unittest.TestCase):
	def test_get_files_info(self):
		# a = get_files_info("calculator", ".")
		# b = get_files_info("calculator", "pkg")
		# c = get_files_info("calculator", "/bin")
		# d = get_files_info("calculator", "../")
		
		# print(a)
		# print(b)
		# print(c)
		# print(d)
		pass

	def test_get_file_content(self):
		# a = get_file_content("calculator", "lorem.txt")
		a = get_file_content("calculator", "main.py")
		b = get_file_content("calculator", "pkg/calculator.py")
		c = get_file_content("calculator", "/bin/cat")

		print(a)
		print(b)
		print(c)
		
if __name__ == "__main__":
	unittest.main()