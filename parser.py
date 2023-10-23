class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return False

    def __repr__(self):
        return f'Token({self.type}, {self.value})'


class Lexer:
    def __init__(self, input):
        self.input = input
        self.position = 0

    #Return List of Tokens
    def tokenize(self):
        n = len(self.input)
        curr_val = ""
        curr_type = ""
        tokens = []
        while self.position < n:
            curr_char = self.input[self.position]
            if curr_char.isalpha():
                #For alphabets
                if curr_type == "INTEGER":
                    #If current token is an integer, add it to list and start a new token
                    prev_token = Token(curr_type, int(curr_val))
                    tokens.append(prev_token)
                    curr_val = curr_char
                elif curr_type == "VARIABLE":
                    #If current token is a variable, append this character to the token string
                    curr_val+= curr_char
                else:
                    curr_val = curr_char
                curr_type = "VARIABLE"
            elif curr_char.isdigit():
                #Process numbers
                if curr_type == "INTEGER":
                    #If current token is an integer, append this number to end
                    curr_val+= curr_char
                elif curr_type == "VARIABLE":
                    #If current token is a variable, add it to list and start a new token
                    prev_token = Token(curr_type, curr_val)
                    tokens.append(prev_token)
                    curr_val = curr_char
                else:
                    curr_val = curr_char
                curr_type = "INTEGER"
            else:
                #If previous token was integer or variable, add to list before processing new token
                if curr_type  == "INTEGER":
                    prev_token = Token(curr_type, int(curr_val))
                    tokens.append(prev_token)
                elif curr_type  == "VARIABLE":
                    prev_token = Token(curr_type, curr_val)
                    tokens.append(prev_token)
                if curr_char in ["+", "-", "*", "/"]:
                    curr_type = "OPERATOR"
                elif curr_char == "=":
                    curr_type = "ASSIGN"
                elif curr_char == ";":
                    curr_type = "SEMICOLON"
                elif curr_char == "(":
                    curr_type = "PARENTHESIS"
                elif curr_char == ")":
                    curr_type = "PARENTHESIS"
                #For whitespace move to next character but don't process
                elif curr_char in [" ", "\n"]:
                    self.position+=1
                    curr_type, curr_val = "", ""
                    continue
                else:
                    raise Exception(f"Invalid character {curr_char}")
                curr_val = curr_char
                curr_token = Token(curr_type, curr_val)
                tokens.append(curr_token)
            self.position+=1
        return tokens
    
class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __str__(self, level=0):
        ret = "\t" * level + f'{self.type}: {self.value}\n'
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.root = None

    def consume(self, expected_type=None):
        if self.position >= len(self.tokens):
            raise Exception("Syntax error: unexpected end of input")
        next_token = self.tokens[self.position]
        if expected_type is None or next_token.type == expected_type:
            self.position+=1
            return next_token
        raise Exception(f"Syntax error: unexpected token {next_token.type}, expected {expected_type}")
    
    def peek(self):
        if self.position >= len(self.tokens):
            raise Exception("Syntax error: unexpected end of input")
        return self.tokens[self.position]
    
    def create_node(self,token: Token):
        return Node(token.type, token.value)
    
    def parse(self):
        #Construct the root of the Abstract Syntax Tree (AST) and iteratively parse each statement in the token list.
        #Root node will be StatementList, each statement will be a child
        root = Node("StatementList", "")
        next_node = self.parse_statement()
        while next_node is not None:
            root.children.append(next_node)
            next_node = self.parse_statement()
        return root

    def parse_statement(self):
        #Check if tokens left, if none left return None
        try:
            self.peek()
        except:
            return None
        return self.parse_assignment()

    def parse_assignment(self): 
        #Parse VARIABLE ASSIGN Expression SEMICOLON
        #Create node of type assignment and assign children
        node = Node("Assignment", "")
        var_token = self.consume("VARIABLE")
        var_node = self.create_node(var_token)
        node.children.append(var_node)
        #Assignment token not needed for AST
        self.consume("ASSIGN")
        node.children.append(self.parse_expression())
        #Semicolon not needed for AST
        self.consume("SEMICOLON")
        return node

    def parse_expression(self):
        next_token = self.peek()
        node = Node("Expression", "")
        #Either parenthesis expression or operation
        if next_token.value == "(":
            #Parse ( Expression ) or ( Expression ) Operator Term
            node.children.append(self.create_node(self.consume("PARENTHESIS")))
            node.children.append(self.parse_expression())
            if not (self.peek().value == ")"):
                raise Exception(f"Expected )")
            node.children.append(self.create_node(self.consume("PARENTHESIS")))
            #Check if of type ( Expression ) Operator Term and parse
            if self.peek().type == "OPERATOR":
                exp_node = node
                node = self.create_node(self.consume("OPERATOR"))
                node.children.append(exp_node)
                node.children.append(self.parse_term())
        else:
            # Parse Expression Operator Term | Term Operator Term | Term
            op1 = self.parse_term()
            if self.peek().type == "OPERATOR":
                #Parse Term Operator Term
                node = self.create_node(self.consume("OPERATOR"))
                node.children.append(op1)
                op2 = self.parse_expression()
                node.children.append(op2)
            else:
                #Parse term
                node = op1
        return node


    def parse_term(self):
        #Create and return term node
        term = self.consume()
        if not (term.type in ["INTEGER", "VARIABLE"]):
            raise Exception(f"Syntax error: Term is of type: {term.type}, expected Integer or Variable")
        node = Node(type=term.type, value=term.value, children=None)
        return node