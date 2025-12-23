import re

class TokenType:
    BHAI = 'BHAI'
    BOL = 'BOL'
    AGAR = 'AGAR'
    NAHI_TOH = 'NAHI_TOH'
    JAB_TAK = 'JAB_TAK'
    HAR_EK = 'HAR_EK'
    KAAM = 'KAAM'
    WAPAS = 'WAPAS'
    KOSHISH = 'KOSHISH'
    GALTI_SE = 'GALTI_SE'
    SAHI = 'SAHI'
    GALAT = 'GALAT'
    AUR = 'AUR'
    YA = 'YA'
    NAHI = 'NAHI'
    BAS_KAR = 'BAS_KAR'
    AAGE_BADH = 'AAGE_BADH'

    JOD = 'JOD'
    GHATA = 'GHATA'
    GUNA = 'GUNA'
    BHAG_KAR = 'BHAG_KAR'

    NUMBER = 'NUMBER'
    STRING = 'STRING'
    IDENTIFIER = 'IDENTIFIER'

    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    EQUALS = 'EQUALS'
    BARABAR = 'BARABAR' 
    BADA = 'BADA'  
    CHOTA = 'CHOTA'  
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    LBRACKET = 'LBRACKET'
    RBRACKET = 'RBRACKET'
    COMMA = 'COMMA'
    SEMICOLON = 'SEMICOLON'
    COLON = 'COLON'
    DOT = 'DOT'

    NEWLINE = 'NEWLINE'
    EOF = 'EOF'

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}:{self.column})"

class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

        self.keywords = {
            'bhai': TokenType.BHAI,
            'bol': TokenType.BOL,
            'agar': TokenType.AGAR,
            'nahi_toh': TokenType.NAHI_TOH,
            'jab_tak': TokenType.JAB_TAK,
            'har_ek': TokenType.HAR_EK,
            'kaam': TokenType.KAAM,
            'wapas': TokenType.WAPAS,
            'koshish': TokenType.KOSHISH,
            'galti_se': TokenType.GALTI_SE,
            'sahi': TokenType.SAHI,
            'galat': TokenType.GALAT,
            'aur': TokenType.AUR,
            'ya': TokenType.YA,
            'nahi': TokenType.NAHI,
            'bas_kar': TokenType.BAS_KAR,
            'aage_badh': TokenType.AAGE_BADH,
            'jod': TokenType.JOD,
            'ghata': TokenType.GHATA,
            'guna': TokenType.GUNA,
            'bhag_kar': TokenType.BHAG_KAR,
            'in': 'IN',
            'barabar': TokenType.BARABAR,
            'bada': TokenType.BADA,
            'chota': TokenType.CHOTA,
        }
    
    def error(self, msg):
        raise SyntaxError(f"Line {self.line}, Column {self.column}: {msg}\n"
                         f"Bhai, type karna nahi aata kya? 😤")
    
    def current_char(self):
        if self.pos >= len(self.code):
            return None
        return self.code[self.pos]
    
    def peek_char(self, offset=1):
        pos = self.pos + offset
        if pos >= len(self.code):
            return None
        return self.code[pos]
    
    def advance(self):
        if self.pos < len(self.code):
            if self.code[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self):
        num_str = ''
        start_col = self.column
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            num_str += self.current_char()
            self.advance()
        
        return Token(TokenType.NUMBER, float(num_str) if '.' in num_str else int(num_str), 
                    self.line, start_col)
    
    def read_string(self):
        start_col = self.column
        quote_char = self.current_char()
        self.advance() 
        
        string = ''
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() == 'n':
                    string += '\n'
                elif self.current_char() == 't':
                    string += '\t'
                else:
                    string += self.current_char()
            else:
                string += self.current_char()
            self.advance()
        
        if not self.current_char():
            self.error("Bhai, string khatam karna bhool gaye! Closing quote daalo!")
        
        self.advance() 
        return Token(TokenType.STRING, string, self.line, start_col)
    
    def read_identifier(self):
        start_col = self.column
        ident = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            ident += self.current_char()
            self.advance()
        
        token_type = self.keywords.get(ident, TokenType.IDENTIFIER)
        return Token(token_type, ident, self.line, start_col)
    
    def tokenize(self):
        while self.current_char():
            self.skip_whitespace()
            self.skip_comment()
            
            if not self.current_char():
                break
            
            char = self.current_char()
            col = self.column

            if char.isdigit():
                self.tokens.append(self.read_number())
            elif char in '"\'':
                self.tokens.append(self.read_string())

            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())

            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.line, col))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', self.line, col))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', self.line, col))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', self.line, col))
                self.advance()
            elif char == '=':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.BARABAR, '==', self.line, col))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.EQUALS, '=', self.line, col))
                    self.advance()
            elif char == '>':
                self.tokens.append(Token(TokenType.BADA, '>', self.line, col))
                self.advance()
            elif char == '<':
                self.tokens.append(Token(TokenType.CHOTA, '<', self.line, col))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, col))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, col))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', self.line, col))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', self.line, col))
                self.advance()
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, '[', self.line, col))
                self.advance()
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ']', self.line, col))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, col))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', self.line, col))
                self.advance()
            elif char == ':':
                self.tokens.append(Token(TokenType.COLON, ':', self.line, col))
                self.advance()
            elif char == '.':
                self.tokens.append(Token(TokenType.DOT, '.', self.line, col))
                self.advance()
            elif char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\\n', self.line, col))
                self.advance()
            else:
                self.error(f"Ye '{char}' kya hai bhai? Invalid character!")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
