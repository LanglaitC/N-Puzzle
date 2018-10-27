import unittest;
from parse import *;

test = [[1, 3, 2], [0, 4, 6], [8, 7, 5]];

class TestParseFile(unittest.TestCase):
    
    def test_valid_3x3(self):
        self.assertEqual([[1, 3, 2], [0, 4, 6], [8, 7, 5]], parse_file("testFiles/valids/3x3.txt"));
    
    def test_valid_3x3_with_comments(self):
        self.assertEqual([[1, 3, 2], [0, 4, 6], [8, 7, 5]], parse_file("testFiles/valids/3x3_comment.txt"));
    
    def test_empty_file(self):
        with self.assertRaises(Exception) as context:
            parse_file("testFiles/invalids/empty_file.txt");
        self.assertTrue("File is not valid format" in context.exception);

    def test_only_comment(self):
        with self.assertRaises(Exception) as context:
            parse_file("testFiles/invalids/only_comment.txt")
        self.assertTrue("File is not valid format" in context.exception);

    def test_one_dimension_taquin(self):
        with self.assertRaises(Exception) as context:
            self.assertRaises(parse_file("testFiles/invalids/1x1_taquin.txt"));
        self.assertTrue("File is not valid format" in context.exception);

    def test_splited_3x3(self):
        with self.assertRaises(Exception) as context:
            self.assertRaises(parse_file("testFiles/invalids/splited_3x3.txt"));
        self.assertTrue("Lign is empty" in context.exception);

if __name__ == '__main__':
    unittest.main();
