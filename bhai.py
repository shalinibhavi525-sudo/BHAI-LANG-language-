import sys
from tokenizer import Tokenizer
from parser import Parser
from interpreter import BhaiInterpreter

def run_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()

        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        interpreter = BhaiInterpreter()
        interpreter.execute(ast)
        
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' nahi mili bhai!")
        print("Sahi path daalo! 📁")
    except SyntaxError as e:
        print(f"❌ Syntax Error:\n{e}")
    except RuntimeError as e:
        print(f"❌ Runtime Error:\n{e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print("Bhai, kuch toh gadbad hai! 😰")

def repl():
    print("=" * 50)
    print("🇮🇳  BHAI-LANG REPL v0.1.0  🇮🇳")
    print("=" * 50)
    print("Namaste! Type 'bye' to exit.")
    print("Type 'help' for examples.")
    print()
    
    interpreter = BhaiInterpreter()
    
    while True:
        try:
            code = input(">>> ")
            
            if code.strip() == "bye":
                print("Phir milenge, bhai! 👋")
                break
            
            if code.strip() == "help":
                print_help()
                continue
            
            if not code.strip():
                continue

            tokenizer = Tokenizer(code)
            tokens = tokenizer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            interpreter.execute(ast)
            
        except KeyboardInterrupt:
            print("\nBye bhai!")
            break
        except EOFError:
            print("\nPhir milenge!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def print_help():
    print("""
📖 BHAI-LANG QUICK REFERENCE:

Print:          bhai bol("Hello!");
Variables:      bhai x = 10;
Math:           bhai bol(jod(5, 3));   // 8
If/Else:        agar (x > 5) { ... } nahi_toh { ... }
While:          jab_tak (x < 10) { ... }
Functions:      kaam greet(naam) { bhai bol(naam); }

Examples:
  bhai bol("Namaste!");
  bhai x = 5;
  bhai y = 10;
  bhai bol(jod(x, y));
  
  agar (x bada 3) {
      bhai bol("X is big!");
  }
""")

def main():
    if len(sys.argv) < 2:
        repl()
    else:
        filename = sys.argv[1]
        run_file(filename)

if __name__ == "__main__":
    main()
