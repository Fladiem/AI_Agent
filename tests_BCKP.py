from functions.get_files_info import get_files_info
import unittest


class TestGet_Files_Info(unittest.TestCase): #gfi == get_files_info
    def test_1(self):  #name must start with test
        output = get_files_info("calculator", ".")
        self.assertTrue(str(output).startswith("Result"))
        
        lines = output.split('\n')
        self.assertTrue("current directory" in lines[0])
        for i in range(1, len(lines)):
            self.assertTrue(lines[i].startswith("- "))
            self.assertTrue('file_size=' in lines[i])
            self.assertTrue(lines[i].endswith('is_dir=False') or lines[i].endswith('is_dir=True'))
    def test_2(self):
        output = get_files_info("calculator", "pkg")
        self.assertTrue(str(output).startswith("Result"))
        
        lines = output.split('\n')
        self.assertTrue("pkg" in lines[0])
        for i in range(1, len(lines)):
            self.assertTrue(lines[i].startswith("- "))
            self.assertTrue('file_size=' in lines[i])
            self.assertTrue(lines[i].endswith('is_dir=False') or lines[i].endswith('is_dir=True'))
    def test_3(self):
        output = get_files_info("calculator", "/bin")
        expected = 'Error: Cannot list "/bin" as it is outside the permitted working directory'
        #with self.assertRaises(SystemExit) as context: ##error raised in previous iteration was not exception, rather sys.exit
            #get_files_info("calculator", "/bin") ##perhaps find workable solution with this format later?  
        #self.assertTrue(str(expected) in str(context.exception))
        self.assertEqual(output, expected)
    def test_4(self):
        output = get_files_info("calculator", "../")
        expected = 'Error: Cannot list "../" as it is outside the permitted working directory'
        self.assertEqual(output, expected)
    def test_5(self):
        output = get_files_info("calculator", "spaghetti")
        expected = 'Error: "calculator/spaghetti" is not a directory' 
        self.assertEqual(output, expected)

""" def test_ParentNode_without_child(self): ####From unittest in static_site_generator, as reference for error tests
        #self.assertEqual does not work here because Errors do not return the error as a value.
        node = ParentNode("p", None)
        
        with self.assertRaises(ValueError) as context:  #asserts that an error is being raised, context becomes ValueError string
            node.to_html()  #specifies the function an Error is expected from
        
        self.assertTrue("Parent node must have children argument" in str(context.exception))
        #checks node.to_html() against "Parent node must have child argument"""


if __name__ == "__main__":
    unittest.main()