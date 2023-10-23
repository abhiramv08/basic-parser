# basic-parser
A parser and lexer in Python for a simple language

Below is the description of the language

Tokens
VARIABLE: Represents variable identifiers and consists of alphabetic characters.
INTEGER: Represents integer literals.
OPERATOR: Represents arithmetic operators, specifically +, -, *, /.
ASSIGN: Represents the assignment operator =.
SEMICOLON: Represents the semicolon ; used to denote the end of a statement.
PARENTHESIS: Represents open ( and close ) parentheses used for grouping.

Grammar
Program -> StatementList
StatementList -> Statement StatementList | Statement
Statement -> AssignmentStatement
AssignmentStatement -> VARIABLE ASSIGN Expression SEMICOLON
Expression -> (Expression) | Expression OPERATOR Term | Term
Term -> INTEGER | VARIABLE
