from parser import *
from tokenizer import TokenType

class BhaiInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
    
    def error(self, msg):
        raise RuntimeError(f"❌ Runtime Error: {msg}\n"
                          f"Bhai, pagal ho gaya hai apna code! 🤦‍♂️")
    
    def execute(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                result = self.execute(statement)
                if result == "break":
                    break
            return None
        
        elif isinstance(node, BhaiStatement):
            value = self.evaluate(node.value)
            self.variables[node.name] = value
            return None
        
        elif isinstance(node, Assignment):
            value = self.evaluate(node.value)
            self.variables[node.name] = value
            return None
        
        elif isinstance(node, BolStatement):
            value = self.evaluate(node.expression)
            print(value)
            return None
        
        elif isinstance(node, IfStatement):
            condition = self.evaluate(node.condition)
            
            if self.is_truthy(condition):
                for stmt in node.then_block:
                    result = self.execute(stmt)
                    if isinstance(result, Return):
                        return result
            elif node.else_block:
                for stmt in node.else_block:
                    result = self.execute(stmt)
                    if isinstance(result, Return):
                        return result
            
            return None
        
        elif isinstance(node, WhileLoop):
            while self.is_truthy(self.evaluate(node.condition)):
                for stmt in node.body:
                    result = self.execute(stmt)
                    if result == "break":
                        return None
                    if isinstance(result, Return):
                        return result
            return None
        
        elif isinstance(node, FunctionDef):
            self.functions[node.name] = node
            return None
        
        elif isinstance(node, Return):
            return Return(self.evaluate(node.value))
        
        elif node == "break":
            return "break"
        
        else:
            return self.evaluate(node)
    
    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value
        
        elif isinstance(node, String):
            return node.value
        
        elif isinstance(node, Identifier):
            if node.name not in self.variables:
                self.error(f'Variable "{node.name}" ko pehle define karo bhai! '
                          f'Ye kya undefined variable use kar rahe ho? 📚')
            return self.variables[node.name]
        
        elif isinstance(node, BinaryOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            op = node.op.type
            
            if op == TokenType.PLUS:
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            
            elif op == TokenType.MINUS:
                if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                    self.error("Bhai, numbers ka hi subtraction hota hai! "
                             "String se kya ghata rahe ho? 🤷‍♂️")
                return left - right
            
            elif op == TokenType.MULTIPLY:
                if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                    self.error("Bhai, numbers ka hi multiplication hota hai!")
                return left * right
            
            elif op == TokenType.DIVIDE:
                if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                    self.error("Bhai, numbers ka hi division hota hai!")
                if right == 0:
                    self.error("Arre bhai! Zero se divide kar rahe ho? "
                             "Maths class mein soye the kya? 💤")
                return left / right
            
            elif op == TokenType.BARABAR:
                return 1 if left == right else 0
            
            elif op == TokenType.BADA:
                return 1 if left > right else 0
            
            elif op == TokenType.CHOTA:
                return 1 if left < right else 0
            
            else:
                self.error(f"Unknown operator: {op}")
        
        elif isinstance(node, UnaryOp):
            operand = self.evaluate(node.operand)
            if node.op.type == TokenType.MINUS:
                return -operand
        
        elif isinstance(node, FunctionCall):
            # Built-in functions
            if node.name == "range":
                if len(node.args) == 1:
                    return list(range(int(self.evaluate(node.args[0]))))
                elif len(node.args) == 2:
                    return list(range(int(self.evaluate(node.args[0])), 
                                    int(self.evaluate(node.args[1]))))
                elif len(node.args) == 3:
                    return list(range(int(self.evaluate(node.args[0])), 
                                    int(self.evaluate(node.args[1])),
                                    int(self.evaluate(node.args[2]))))

            if node.name not in self.functions:
                self.error(f'Function "{node.name}" define hi nahi hai bhai! '
                          f'Pehle define karo phir call karo! 🤔')
            
            func = self.functions[node.name]
            
            if len(node.args) != len(func.params):
                self.error(f'Function "{node.name}" ko {len(func.params)} arguments chahiye, '
                          f'tumne {len(node.args)} diye! Count toh sahi karo! 🔢')

            old_vars = self.variables.copy()

            for param, arg in zip(func.params, node.args):
                self.variables[param] = self.evaluate(arg)

            result = None
            for stmt in func.body:
                exec_result = self.execute(stmt)
                if isinstance(exec_result, Return):
                    result = exec_result.value
                    break

            self.variables = old_vars
            
            return result
        
        elif isinstance(node, ListLiteral):
            return [self.evaluate(elem) for elem in node.elements]
        
        else:
            self.error(f"Cannot evaluate: {type(node)}")
    
    def is_truthy(self, value):
        if value == 0 or value == "" or value is None:
            return False
        return True
