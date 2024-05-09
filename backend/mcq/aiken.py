import collections

import ply.lex as lex
import ply.yacc as yacc


tokens = ('ANSWER', 'OPTION', 'ANY', 'FEEDBACK')

t_ANSWER = r'ANSWER:\s*[a-zA-Z]'
t_OPTION = r'[a-zA-Z][.)]\s'
t_ANY = r'.*\n'
t_FEEDBACK = r'FEEDBACK:\s*.*'

# t_ignore = '\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def p_question(p):
    'question : cmd options answer ANY feedback'
    p[0] = (p[1].rstrip(), p[2], p[3], p[5])

def p_cmd(p):
    '''cmd : cmd ANY
           | ANY'''
    p[0] = p[1] + p[2] if len(p) > 2 else p[1]

def p_options(p):
    '''options : options option
               | option'''
    p[0] = p[1] + [p[2]] if len(p) > 2 else [p[1]]

def p_option(p):
    'option : OPTION ANY'
    p[0] = (p[1].strip(), p[2].strip())

def p_answer(p):
    'answer : ANSWER'
    p[0] = p[1][7:].strip()

def p_feedback(p):
    'feedback : FEEDBACK'
    p[0] = p[1][9:].strip()

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}")
        print(f"Error type: Unexpected {p.type}")
        print(f"Error position: {p.lexpos}")
        print(f"Entire p object: {p}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

class Aiken(list):
    """
    Represents the result of parsing an Aiken string.
    """
    def __init__(self):
        self.question = ""
        self.full_options = {}
        self.options = []
        self.answer = ""
        self.feedback = ""

    def append(self, s):
        ord_dict = collections.OrderedDict(sorted(self.full_options.items(), key=lambda t: t[0]))
        option_letter = list(ord_dict.keys())[-1] # Gets the last alphabetic letter from options
        next_letter = ""
        if(")" in option_letter):
            next_letter = chr(ord(option_letter.rstrip(')'))+1)
            next_letter += ")"
        else:
            next_letter = chr(ord(option_letter.rstrip('.'))+1)
            next_letter += "."
        print("Proxima letra: ", next_letter)
        self.full_options.update({next_letter: s})

    def __str__(self):
        string = ''

        string += self.question + '\n'
        for option in self.options:
            # string += option.key + '.' + option.value + '\n'
            string += option + '\n'

        string += 'ANSWER: ' + self.answer + '\n'
        string += 'FEEDBACK: ' + self.feedback
        return string

def load(file_or_string):
    """
    Load a file or string in the Aiken format and return a parsed object.

    Args:
        file_or_string:
            A file object containing the Aiken source or a string.

    Returns:
        An :cls:`Aiken` instance.
    """
    aiken = Aiken()
    try:
        file_obj = open(file_or_string)
        content = file_obj.read()
        file_obj.close()
    except OSError:
        content = file_or_string

    try:
        lexer.input(content)
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
        ast = parser.parse(content, lexer=lexer)
    except SyntaxError as e:
        print(f"Syntax error while parsing content: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error while parsing content: {e}")
        return None

    if ast is None:
        print("Failed to parse content")
        return None
    for options in ast[1]:
        for i in range(len(options)):
            if ((i+1) < len(options)):
                aiken.full_options[options[i]] = options[i+1]

    aiken.options = list(aiken.full_options.values())
    aiken.answer = ast[2]
    aiken.question = ast[0]
    aiken.feedback = ast[3]
    return aiken

def dump(aiken, file=None):
    """
    Writes aiken object in the given file. If no file is given, return a string
    with the file contents.
    """
    aiken_content = ""

    aiken_content += aiken.question + "\n"
    aiken_dict = aiken.full_options
    for k, v in sorted(aiken_dict.items()):
        aiken_content += k + " " + v + "\n"

    aiken_content += "ANSWER: " +aiken.answer
    aiken_content += "FEEDBACK: " +aiken.feedback

    if file is not None:
        file = open(file, "w")
        file.write(aiken_content)
        file.close()
        return ""
    else:
        return aiken_content

    return aiken_content

# aiken_with_string = load("""Is this a valid Aiken Question?
# A. Yes
# B. No
# ANSWER: A
# FEEDBACK: This is a feedback""")
# aiken_with_file = load("aiken_example.txt")
# aiken_with_string.append("Maybe")
# aiken_with_file.append("Shit")
# print(dump(aiken_with_string))
# print(dump(aiken_with_file))
