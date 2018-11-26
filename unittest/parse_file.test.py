import unittest
from parse import *

test = [[1, 3, 2], [0, 4, 6], [8, 7, 5]]

class TestParseFile(unittest.TestCase): 
    def test_valid_3x3(self):
        self.assertEqual([[1, 3, 2], [0, 4, 6], [8, 7, 5]], parse_file("testFiles/valids/3x3.txt"))
    
    def test_valid_3x3_with_comments(self):
        self.assertEqual([[1, 3, 2], [0, 4, 6], [8, 7, 5]], parse_file("testFiles/valids/3x3_comment.txt"))

    def test_valid_3x3_with_comments_inline(self):
        self.assertEqual([[1, 3, 2], [0, 4, 6], [8, 7, 5]], parse_file("testFiles/valids/3x3_comment_inline.txt"))

    
    def test_empty_file(self):
        with self.assertRaises(Exception) as context:
            parse_file("testFiles/invalids/empty_file.txt")
        self.assertTrue("Your taquin should be at least 2x2" in context.exception)

    def test_only_comment(self):
        with self.assertRaises(Exception) as context:
            parse_file("testFiles/invalids/only_comment.txt")
        self.assertTrue("Your taquin should be at least 2x2" in context.exception)

    def test_one_dimension_taquin(self):
        with self.assertRaises(Exception) as context:
            self.assertRaises(parse_file("testFiles/invalids/1x1_taquin.txt"))
        self.assertTrue("Your taquin should be at least 2x2" in context.exception)

    def test_splited_3x3(self):
        with self.assertRaises(Exception) as context:
            self.assertRaises(parse_file("testFiles/invalids/splited_3x3.txt"))
        self.assertTrue("Invalid file, taquin should be a square" in context.exception)
    
    def test_4x3(self):
        with self.assertRaises(Exception) as context:
            self.assertRaises(parse_file("testFiles/invalids/4x3.txt"))
        self.assertTrue("Invalid file, taquin should be a square" in context.exception)

    def test_3x4(self):
        with self.assertRaises(Exception) as context:
            self.assertRaises(parse_file("testFiles/invalids/3x4.txt"))
        self.assertTrue("Invalid file, taquin should be a square" in context.exception)

    def test_out_of_range_3x3(self):
        with self.assertRaises(Exception) as context:
            self.assertRaises(parse_file("testFiles/invalids/out_of_range_3x3.txt"))
        self.assertTrue("Character 9 is out of range should be between 0 and 8, position : (3,3)" in context.exception)

    def test_negative_number_3x3(self):
        with self.assertRaises(Exception) as context:
            self.assertRaises(parse_file("testFiles/invalids/negative_number_3x3.txt"))
        self.assertTrue("Character -1 is out of range should be between 0 and 8, position : (1,1)" in context.exception)
    
    def test_duplicate_character(self):
        with self.assertRaises(Exception) as context:
            self.assertRaises(parse_file("testFiles/invalids/duplicate_character_3x3.txt"))
        self.assertTrue("Duplicate Character 2 at position : (1,3)" in context.exception)


class TestParseLine(unittest.TestCase):
    def test_valid_line(self):
        self.assertEqual(parse_line("1 3 5 6"), [1, 3, 5, 6])
    
    def test_invalid_line(self):
        with self.assertRaises(Exception):
            self.assertRaises(parse_line("1 5 4a 6"))

if __name__ == '__main__':
    unittest.main()
