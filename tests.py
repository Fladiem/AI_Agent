
from functions.get_file_content import get_file_content
import unittest


class TestGet_Files_Content(unittest.TestCase): #gfi == get_files_info
    def test_1(self):  #name must start with test
        output = get_file_content("calculator", "main.py")
        self.assertTrue("def main():" in output and "print('Example: python main.py" in output)
    
    def test_2(self):
        output = get_file_content("calculator", "pkg/calculator.py")
        print(output)
        self.assertTrue("class Calculator:" in output and "def _apply_operator(self, operators, values):" in output)

    def test_3(self):
        output = get_file_content("calculator", "/bin/cat")
        self.assertTrue(output.startswith("Error: Cannot read") and output.endswith("working directory"))
        self.assertTrue("/bin/cat" in output)
    
    def test_4(self):
        output = get_file_content("calculator", "pkg/does_not_exist.py")
        self.assertTrue(output.startswith("Error: File not found or is not a regular file:"))
        self.assertTrue("pkg/does_not_exist.py" in output)
    
    #def test_5(self):
        #output = get_file_content("calculator", "lorem.txt")
        #self.assertTrue('...File "' in output and "lorem.txt" in output and "Vestibulum" in output)
        



if __name__ == "__main__":
    unittest.main()