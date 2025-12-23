from tokenizer import TokenType

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class BhaiStatement(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BolStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class IfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class Return(ASTNode):
    def __init__(self, value):
        self.value = value

class ListLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg):
        token = self.current_token()
        raise SyntaxError(f"Line {token.line}: {msg}\n"
                         f"Bhai, type karna nahi aata kya? 😤")
    
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def peek_token(self, offset=1):
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def advance(self):
        self.pos += 1
    
    def expect(self, token_type):
        if self.current_token().type != token_type:
            self.error(f"Expected {token_type}, got {self.current_token().type}")
        token = self.current_token()
        self.advance()
        return token
    
    def skip_newlines(self):
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self):
        statements = []
        self.skip_newlines()
        
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements)
    
    def parse_statement(self):
        self.skip_newlines()
        token = self.current_token()

        if token.type == TokenType.BHAI:
            return self.parse_bhai_statement()

        elif token.type == TokenType.AGAR:
            return self.parse_if_statement()

        elif token.type == TokenType.JAB_TAK:
            return self.parse_while_loop()

        elif token.type == TokenType.KAAM:
            return self.parse_function_def()

        elif token.type == TokenType.WAPAS:
            return self.parse_return()

        elif token.type == TokenType.BAS_KAR:
            self.advance()
            return "break"

        elif token.type == TokenType.IDENTIFIER:
            if self.peek_token().type == TokenType.EQUALS:
                name = token.value
                self.advance()
                self.expect(TokenType.EQUALS)
                value = self.parse_expression()
                return Assignment(name, value)
            else:
                return self.parse_expression()
        
        else:
            return self.parse_expression()
    
    def parse_bhai_statement(self):
        self.expect(TokenType.BHAI)

        if self.current_token().type == TokenType.BOL:
            self.advance()
            self.expect(TokenType.LPAREN)
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return BolStatement(expr)

        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.EQUALS)
        value = self.parse_expression()
        
        return BhaiStatement(name_token.value, value)
    
    def parse_if_statement(self):
        self.expect(TokenType.AGAR)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        then_block = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                then_block.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        self.skip_newlines()
        
        # Check for else
        else_block = None
        if self.current_token().type == TokenType.NAHI_TOH:
            self.advance()
            self.expect(TokenType.LBRACE)
            self.skip_newlines()
            
            else_block = []
            while self.current_token().type != TokenType.RBRACE:
                stmt = self.parse_statement()
                if stmt:
                    else_block.append(stmt)
                self.skip_newlines()
            
            self.expect(TokenType.RBRACE)
        
        return IfStatement(condition, then_block, else_block)
    
    def parse_while_loop(self):
        self.expect(TokenType.JAB_TAK)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        body = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        return WhileLoop(condition, body)
    
    def parse_function_def(self):
        self.expect(TokenType.KAAM)
        name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        params = []
        
        if self.current_token().type != TokenType.RPAREN:
            params.append(self.expect(TokenType.IDENTIFIER).value)
            
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                params.append(self.expect(TokenType.IDENTIFIER).value)
        
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        body = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        return FunctionDef(name, params, body)
    
    def parse_return(self):
        self.expect(TokenType.WAPAS)
        value = self.parse_expression()
        return Return(value)
    
    def parse_expression(self):
        return self.parse_comparison()
    
    def parse_comparison(self):
        left = self.parse_additive()
        
        while self.current_token().type in [TokenType.BARABAR, TokenType.BADA, TokenType.CHOTA]:
            op = self.current_token()
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token()
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self):
        left = self.parse_unary()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op = self.current_token()
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self):
        if self.current_token().type == TokenType.MINUS:
            op = self.current_token()
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_primary()
    
    def parse_primary(self):
        token = self.current_token()
        
        # Numbers
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(token.value)
        
        # Strings
        elif token.type == TokenType.STRING:
            self.advance()
            return String(token.value)
        
        # Boolean literals
        elif token.type == TokenType.SAHI:
            self.advance()
            return Number(1) 
        
        elif token.type == TokenType.GALAT:
            self.advance()
            return Number(0) 

        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr

        elif token.type == TokenType.LBRACKET:
            self.advance()
            elements = []
            
            if self.current_token().type != TokenType.RBRACKET:
                elements.append(self.parse_expression())
                
                while self.current_token().type == TokenType.COMMA:
                    self.advance()
                    elements.append(self.parse_expression())
            
            self.expect(TokenType.RBRACKET)
            return ListLiteral(elements)

        elif token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()

            if self.current_token().type == TokenType.LPAREN:
                self.advance()
                args = []
                
                if self.current_token().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    
                    while self.current_token().type == TokenType.COMMA:
                        self.advance()
                        args.append(self.parse_expression())
                
                self.expect(TokenType.RPAREN)
                return FunctionCall(name, args)

            return Identifier(name)

        elif token.type == TokenType.JOD:
            self.advance()
            self.expect(TokenType.LPAREN)
            left = self.parse_expression()
            self.expect(TokenType.COMMA)
            right = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return BinaryOp(left, Token(TokenType.PLUS, '+', 0, 0), right)
        
        elif token.type == TokenType.GHATA:
            self.advance()
            self.expect(TokenType.LPAREN)
            left = self.parse_expression()
            self.expect(TokenType.COMMA)
            right = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return BinaryOp(left, Token(TokenType.MINUS, '-', 0, 0), right)
        
        elif token.type == TokenType.GUNA:
            self.advance()
            self.expect(TokenType.LPAREN)
            left = self.parse_expression()
            self.expect(TokenType.COMMA)
            right = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return BinaryOp(left, Token(TokenType.MULTIPLY, '*', 0, 0), right)
        
        elif token.type == TokenType.BHAG_KAR:
            self.advance()
            self.expect(TokenType.LPAREN)
            left = self.parse_expression()
            self.expect(TokenType.COMMA)
            right = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return BinaryOp(left, Token(TokenType.DIVIDE, '/', 0, 0), right)
        
        else:
            self.error(f"Unexpected token: {token.type}")
