
from functions.run_python_file import run_python_file
import subprocess
import os
import unittest


class TestRun_Python_File(unittest.TestCase):
    def test1(self):
        output = run_python_file("calculator", "main.py")
        print("test1", output)

    def test2(self):
        output = run_python_file("calculator", "main.py", ["3 + 5"])
        print("test2", output)

    def test3(self):
        output = run_python_file("calculator", "tests.py")
        print("test3", output)

    def test4(self):
        output = run_python_file("calculator", "../main.py")
        print("test4", output)
    
    def test5(self):
        output = run_python_file("calculator", "nonexistent.py")
        print("test5", output)

    def test6(self):
        output = run_python_file("calculator", "lorem.txt", 5)
        print("test6", output)
        print("REMINDER: These tests require manual verification, automated results are not informed by evaluators")
    
    


    
        



if __name__ == "__main__":
    unittest.main()