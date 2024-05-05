from lark import Lark, Transformer, v_args


aiken_grammar = """
    start: question
    question: cmd options answer feedback
    cmd: ANY
    options: option+
    option: OPTION ANY
    answer: "ANSWER:" ANY
    feedback: "FEEDBACK:" ANY
    OPTION: /[a-zA-Z][.)]/
    ANY: /.*\n/
"""

class AikenTransformer(Transformer):
    @v_args(inline=True)
    def question(self, cmd, options, answer, feedback):
        return cmd, options, answer[1:], feedback[1:]

    def option(self, items):
        return items[1]

    def ANY(self, items):
        return items[0].rstrip()

    def OPTION(self, items):
        return items[0].rstrip()

aiken_parser = Lark(aiken_grammar, parser='lalr', transformer=AikenTransformer())

def load(content):
    """
    Load a string in the Aiken format and return a parsed object.

    Args:
        content: A string in the Aiken format.

    Returns:
        A list of tuples representing the parsed data.
    """
    try:
        ast = aiken_parser.parse(content)
    except Exception as e:
        print(f"Unexpected error while parsing content: {e}")
        return None

    if ast is None:
        print("Failed to parse content")
        return None

    return ast
