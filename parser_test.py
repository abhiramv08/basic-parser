import unittest
from parser import Lexer, Parser, Token, Node 


class CustomTextTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.passed_tests = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        self.passed_tests += 1

    def print_result(self):
        total_tests = self.testsRun
        if total_tests == 0:
            print("No tests were run.")
            return
        print(f"\nPassed {self.passed_tests} out of {total_tests} tests")

class CustomTextTestRunner(unittest.TextTestRunner):
    def __init__(self, stream=None, descriptions=True, verbosity=1, failfast=False,
                 buffer=False, resultclass=None, warnings=None, *, tb_locals=False):
        resultclass = CustomTextTestResult
        super().__init__(stream, descriptions, verbosity, failfast, buffer, resultclass, warnings, tb_locals=tb_locals)

    def run(self, test):
        result = super().run(test)
        result.print_result()
        return result


class TestLexerParser(unittest.TestCase):

    def test_lexer(self):
        input_code = "a = 5 + 3;"
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()
        expected_tokens = [
            Token('VARIABLE', 'a'),
            Token('ASSIGN', '='),
            Token('INTEGER', 5),
            Token('OPERATOR', '+'),
            Token('INTEGER', 3),
            Token('SEMICOLON', ';')
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_parser_valid_input(self):
        input_code = "a = 5;"
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            ast = parser.parse()
            self.assertIsInstance(ast, Node)
            print(f"AST for {input_code} is {ast}")
        except Exception as e:
            self.fail(f"Test failed with valid input due to {e}")
    def test_parser_multi_line(self):
        input_code = """
        a = 5 + 3;
        b = a * 2;
        c = a + b;
        """
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            ast = parser.parse()
            self.assertIsInstance(ast, Node)
            print(f"AST for multi-line input is {ast}")
        except Exception as e:
            self.fail(f"Test failed with multi-line valid input due to {e}")

    def test_parser_multiple_operations(self):
        input_code = """
        a = 5 + 3;
        b = a * 2 - 1;
        c = (a + b) * 2;
        """
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            ast = parser.parse()
            self.assertIsInstance(ast, Node)
            print(f"AST for {input_code} is {ast}")
        except Exception as e:
            self.fail(f"Test case failed: {e}")

    def test_parser_nested_expressions(self):
        input_code = """
        a = ((5 + 3) * 2) - 1;
        b = 2 * (a + 1);
        """
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            ast = parser.parse()
            self.assertIsInstance(ast, Node)
            print(f"AST for {input_code} is {ast}")
        except Exception as e:
            self.fail(f"Test failed with nested expressions due to {e}")

    def test_parser_invalid_assignment(self):
        input_code = "5 = a;"
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaises(Exception) as context:
            parser.parse()
        self.assertTrue('Syntax error' in str(context.exception))

    def test_parser_invalid_character(self):
        input_code = "a = % 5;"
        lexer = Lexer(input_code)
        with self.assertRaises(Exception) as context:
            lexer.tokenize()
        self.assertTrue('Invalid character' in str(context.exception))

    def test_parser_invalid_operation(self):
        input_code = "a = (5 + );"
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaises(Exception) as context:
            parser.parse()
        self.assertTrue('Syntax error' in str(context.exception))
    
    def test_parser_invalid_inputs(self):
        input_code = """
        a = 5 + ;
        b = * 2;
        """
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaises(Exception) as context:
            parser.parse()
        self.assertTrue('Syntax error' in str(context.exception))


    def test_missing_semicolon(self):
        input_code = "a = 5"
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaises(Exception) as context:
            parser.parse()
        self.assertTrue('Syntax error: unexpected end of input' in str(context.exception))


if __name__ == '__main__':
    unittest.main(testRunner=CustomTextTestRunner(verbosity=2))