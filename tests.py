# tests.py

import unittest
from functions.get_files_info import get_files_info, get_file_content, write_file

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
		# a = get_file_content("calculator", "main.py")
		# b = get_file_content("calculator", "pkg/calculator.py")
		# c = get_file_content("calculator", "/bin/cat")

		# print(a)
		# print(b)
		# print(c)
		pass

	def test_write_file(self):
		# a = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
		# b = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
		# c = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

		# print(a)
		# print(b)
		# print(c)
		pass
		
		
if __name__ == "__main__":
	unittest.main()