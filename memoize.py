from functools import lru_cache
import ast

import inspect


class ASTWalker(ast.NodeVisitor):
    def visit(self, node, indent=0):
        print("  " * indent, type(node).__name__)
        for child in ast.iter_child_nodes(node):
            self.visit(child, indent + 1)


def walk_ast(code):
    tree = ast.parse(code)
    walker = ASTWalker()
    walker.visit(tree)


# @lru_cache(maxsize=1000)
def fib(n):
    if n <= 1:
        return 0
    elif n == 2:
        return 1
    elif n == 3:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


fibcache = {}


def manually_cached_fib(n):
    if n in fibcache:
        return fibcache[n]
    else:
        if n <= 1:
            return 0
        elif n == 2:
            return 1
        elif n == 3:
            return 1
        else:
            r = manually_cached_fib(n - 1) + manually_cached_fib(n - 2)
            fibcache[n] = r
            return r


def memoize(f):
    cache = {}

    def wrapper(*args, **kwargs):
        if args in cache:
            return cache[args]
        else:
            r = f(*args, **kwargs)
            cache[args] = r
            return r

    return wrapper


def flat_fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def aggro_memoize(f):
    d = {}

    def memoized_version(n):
        if n in d:
            return d[n]
        else:
            r = f(n)
            d[n] = r
            return r

    # reach into internal funccalls and replace them
    f.__globals__[f.__name__] = memoized_version

    return memoized_version


import ast
import inspect


class ReplaceRecursiveCall(ast.NodeTransformer):
    def __init__(self, func_name):
        self.func_name = func_name

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.func_name:
            node.func.id = f"memoized_{self.func_name}"
        return node


def wtf_memoize(f):
    d = {}

    def memoized_version(n):
        if n in d:
            return d[n]
        else:
            r = f(n)
            d[n] = r
            return r

    # Replace recursive calls
    source = inspect.getsource(f)
    dedented_source = source.lstrip()  # Remove leading spaces
    tree = ast.parse(dedented_source)
    transformer = ReplaceRecursiveCall(f.__name__)
    modified_tree = transformer.visit(tree)
    ast.fix_missing_locations(modified_tree)
    exec(compile(modified_tree, filename="<ast>", mode="exec"), f.__globals__)
    f.__globals__[f"memoized_{f.__name__}"] = memoized_version

    return f.__globals__[f"memoized_{f.__name__}"]


mfib = wtf_memoize(fib)
a = mfib(100)
print(a)
# code = inspect.getsource(fib)
# walk_ast(code)
