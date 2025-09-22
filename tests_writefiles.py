
from functions.write_file import write_file
import unittest


class TestWrite_File(unittest.TestCase):
    def test1(self):
        output = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        
        self.assertTrue(output.startswith('Successfully wrote to "'))
        self.assertTrue("lorem.txt" in output)
    
    def test2(self):
        output = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")

        self.assertTrue(output.startswith('Successfully wrote to "'))
        self.assertTrue("pkg/morelorem.txt" in output)
    
    def test3(self):
        output = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

        self.assertTrue(output.startswith("Error:"))
        self.assertTrue("/tmp/temp.txt" in output)
        self.assertTrue(output.endswith("working directory"))


    
        



if __name__ == "__main__":
    unittest.main()