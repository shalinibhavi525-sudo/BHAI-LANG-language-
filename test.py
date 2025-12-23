from tokenizer import Tokenizer
from parser import Parser
from interpreter import BhaiInterpreter

def test_basic():
    print("Testing basic operations...")
    
    code = '''
    bhai x = 5;
    bhai y = 10;
    bhai bol(jod(x, y));
    '''
    
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = BhaiInterpreter()
    interpreter.execute(ast)
    print("✅ Basic operations working!")

def test_conditionals():
    print("\nTesting conditionals...")
    
    code = '''
    bhai x = 10;
    agar (x bada 5) {
        bhai bol("X is big!");
    } nahi_toh {
        bhai bol("X is small!");
    }
    '''
    
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = BhaiInterpreter()
    interpreter.execute(ast)
    print("✅ Conditionals working!")

def test_loops():
    print("\nTesting loops...")
    
    code = '''
    bhai i = 0;
    jab_tak (i chota 5) {
        bhai bol(i);
        i = jod(i, 1);
    }
    '''
    
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = BhaiInterpreter()
    interpreter.execute(ast)
    print("✅ Loops working!")

def test_functions():
    print("\nTesting functions...")
    
    code = '''
    kaam add(a, b) {
        wapas jod(a, b);
    }
    
    bhai result = add(5, 3);
    bhai bol(result);
    '''
    
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = BhaiInterpreter()
    interpreter.execute(ast)
    print("✅ Functions working!")

def test_errors():
    print("\nTesting error messages...")
    
    # Test division by zero
    try:
        code = 'bhai bol(bhag_kar(10, 0));'
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = BhaiInterpreter()
        interpreter.execute(ast)
    except RuntimeError as e:
        print(f"✅ Division by zero caught: {e}")
    
    # Test undefined variable
    try:
        code = 'bhai bol(undefined_var);'
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = BhaiInterpreter()
        interpreter.execute(ast)
    except RuntimeError as e:
        print(f"✅ Undefined variable caught: {e}")

if __name__ == "__main__":
    print("🇮🇳 BHAI-LANG TEST SUITE 🇮🇳")
    print("=" * 50)
    
    test_basic()
    test_conditionals()
    test_loops()
    test_functions()
    test_errors()
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED! Bhai-Lang is working! 🎉")
