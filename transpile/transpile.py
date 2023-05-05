import ast
import inspect
from pprint import pprint
import esprima
import json
import astunparse

from pyast_to_jsast import python_to_js_ast


def convert_python_ast_to_js_ast(python_ast):
    js_ast = {
        "type": "Program",
        "body": [python_to_js_ast(node) for node in python_ast.body],
    }
    return js_ast


# def transpile(python_code):
#     python_ast = ast.parse(python_code)
#     try:
#         js_ast = {
#             "type": "Program",
#             "body": [python_to_js_ast(node) for node in python_ast.body],
#         }
#         return escodegen.generate(js_ast, {"format": {"indent": {"style": "  "}}})

#     except Exception as e:
#         print(json.dumps(js_ast, indent=2))  # Print the JavaScript AST
#         raise e


# Test the transpiler on a simple Python function
def add(x, y):
    return x + y


def more_ops(x, y):
    return x + y * 2


def abs_value(x):
    if x < 0:
        return -x
    else:
        return x


def outer_function(x):
    def inner_function(y):
        return x * y

    return inner_function(x + 1)


def printtest():
    print(1)


def printvar(x):
    print(x)


def fortest(x):
    for i in range(1, x):
        return i


def sum_of_squares(n):
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total


def countdown(x):
    while x > 0:
        print(x)
        x -= 1
    print("Liftoff!")


def reverse_list(lst):
    result = []
    for item in lst:
        result.insert(0, item)
    return result


def test(fs):
    for f in fs:
        python_code = inspect.getsource(f)
        try:
            python_ast = ast.parse(python_code)
            js_ast = convert_python_ast_to_js_ast(python_ast)
            # js_code = transpile(python_code)
            # pprint(js_ast)
            # dump to a file
            with open(f"{f.__name__}.json", "w") as f:
                json.dump(js_ast, f, indent=2)
        except Exception as e:
            print(f"Error Converting ASTs {f.__name__}: {e}")
        print()


fs = [
    add,
    more_ops,
    abs_value,
    outer_function,
    printtest,
    printvar,
    fortest,
    sum_of_squares,
    countdown,
    reverse_list,
]
test(fs)
