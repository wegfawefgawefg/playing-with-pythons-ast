import ast
import astunparse


def python_to_js_ast(node):
    if isinstance(node, ast.FunctionDef):
        return {
            "type": "FunctionDeclaration",
            "id": {"type": "Identifier", "name": node.name},
            "params": [python_to_js_ast(arg) for arg in node.args.args],
            "body": {
                "type": "BlockStatement",
                "body": [python_to_js_ast(stmt) for stmt in node.body],
            },
        }
    elif isinstance(node, ast.Call):
        # special case for print
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            # may also not work
            return {
                "type": "CallExpression",
                "callee": {"type": "Identifier", "name": "console.log"},
                "arguments": [python_to_js_ast(arg) for arg in node.args],
            }

        elif isinstance(node.func, ast.Name) and node.func.id == "range":
            # may not work??
            start = python_to_js_ast(node.args[0])
            end = python_to_js_ast(node.args[1]) if len(node.args) > 1 else None
            step = python_to_js_ast(node.args[2]) if len(node.args) > 2 else None

            return {
                "type": "CallExpression",
                "callee": {"type": "Identifier", "name": "Array.from"},
                "arguments": [
                    {
                        "type": "CallExpression",
                        "callee": {"type": "Identifier", "name": "Array"},
                        "arguments": [
                            {
                                "type": "BinaryExpression",
                                "left": end,
                                "operator": "-",
                                "right": start,
                            }
                        ],
                    },
                    {
                        "type": "ArrowFunctionExpression",
                        "params": [{"type": "Identifier", "name": "_"}],
                        "body": {
                            "type": "BinaryExpression",
                            "left": start,
                            "operator": "+",
                            "right": {
                                "type": "BinaryExpression",
                                "left": {"type": "Identifier", "name": "_"},
                                "operator": "*",
                                "right": (
                                    step if step else {"type": "Literal", "value": 1}
                                ),
                            },
                        },
                        "expression": True,
                    },
                ],
            }

        return {
            "type": "CallExpression",
            "callee": python_to_js_ast(node.func),
            "arguments": [python_to_js_ast(arg) for arg in node.args],
        }
    elif isinstance(node, ast.Name):
        return {"type": "Identifier", "name": node.id}
    elif isinstance(node, ast.arg):
        return {"type": "Identifier", "name": node.arg}
    elif isinstance(node, ast.Return):
        return {"type": "ReturnStatement", "argument": python_to_js_ast(node.value)}
    elif isinstance(node, ast.Num):
        return {"type": "Literal", "value": node.n}
    elif isinstance(node, ast.BinOp):
        return {
            "type": "BinaryExpression",
            "left": python_to_js_ast(node.left),
            "operator": python_to_js_ast(node.op),
            "right": python_to_js_ast(node.right),
        }
    elif isinstance(node, ast.Add):
        return "+"
    elif isinstance(node, ast.Mult):
        return "*"
    elif isinstance(node, ast.Sub):
        return "-"
    elif isinstance(node, ast.Div):
        return "/"
    elif isinstance(node, ast.Lt):
        return "<"
    elif isinstance(node, ast.Gt):
        return ">"
    elif isinstance(node, ast.Eq):
        return "=="
    elif isinstance(node, ast.LtE):
        return "<="
    elif isinstance(node, ast.GtE):
        return ">="
    elif isinstance(node, ast.If):
        return {
            "type": "IfStatement",
            "test": python_to_js_ast(node.test),
            "consequent": python_to_js_ast(node.body[0]),
            "alternate": python_to_js_ast(node.orelse[0]),
        }
    elif isinstance(node, ast.Compare):
        return {
            "type": "BinaryExpression",
            "left": python_to_js_ast(node.left),
            "operator": python_to_js_ast(node.ops[0]),
            "right": python_to_js_ast(node.comparators[0]),
        }
    elif isinstance(node, ast.BoolOp):
        return {
            "type": "LogicalExpression",
            "left": python_to_js_ast(node.values[0]),
            "operator": python_to_js_ast(node.op),
            "right": python_to_js_ast(node.values[1]),
        }
    elif isinstance(node, ast.And):
        return "&&"
    elif isinstance(node, ast.Or):
        return "||"
    elif isinstance(node, ast.While):
        return {
            "type": "WhileStatement",
            "test": python_to_js_ast(node.test),
            "body": python_to_js_ast(node.body),
        }
    elif isinstance(node, ast.Assign):
        return {
            "type": "AssignmentExpression",
            "left": python_to_js_ast(node.targets[0]),
            "operator": "=",
            "right": python_to_js_ast(node.value),
        }
    elif isinstance(node, ast.Expr):
        return python_to_js_ast(node.value)

    elif isinstance(node, ast.For):
        iter_var = python_to_js_ast(node.target)
        start = {"type": "Literal", "value": 0}
        end = python_to_js_ast(node.iter.args[0])
        step = {"type": "Literal", "value": 1}

        return {
            "type": "ForStatement",
            "init": {
                "type": "VariableDeclaration",
                "declarations": [
                    {"type": "VariableDeclarator", "id": iter_var, "init": start}
                ],
                "kind": "let",
            },
            "test": {
                "type": "BinaryExpression",
                "left": iter_var,
                "operator": "<",
                "right": end,
            },
            "update": {
                "type": "AssignmentExpression",
                "operator": "+=",
                "left": iter_var,
                "right": step,
            },
            "body": {
                "type": "BlockStatement",
                "body": [python_to_js_ast(stmt) for stmt in node.body],
            },
        }

    elif isinstance(node, ast.List):
        return {
            "type": "ArrayExpression",
            "elements": [python_to_js_ast(elt) for elt in node.elts],
        }
    elif isinstance(node, ast.Subscript):
        return {
            "type": "MemberExpression",
            "object": python_to_js_ast(node.value),
            "property": python_to_js_ast(node.slice),
            "computed": True,
        }
    elif isinstance(node, ast.Index):
        return python_to_js_ast(node.value)
    elif isinstance(node, ast.Str):
        return {"type": "Literal", "value": node.s}
    # unary op
    elif isinstance(node, ast.UnaryOp):
        return {
            "type": "UnaryExpression",
            "operator": python_to_js_ast(node.op),
            "argument": python_to_js_ast(node.operand),
        }
    elif isinstance(node, ast.USub):
        return "-"
    elif isinstance(node, ast.UAdd):
        return "+"
    elif isinstance(node, ast.Not):
        return "!"
    # augassign
    elif isinstance(node, ast.AugAssign):
        return {
            "type": "AssignmentExpression",
            "left": python_to_js_ast(node.target),
            "operator": python_to_js_ast(node.op),
            "right": python_to_js_ast(node.value),
        }
    # else:
    #     raise ValueError(f"Unsupported node type: {node.__class__.__name__}")
    else:
        source_code_snippet = astunparse.unparse(node).strip()
        raise ValueError(
            f"Unsupported node type: {node.__class__.__name__}\n"
            f"Source code snippet: {source_code_snippet}\n"
            f"AST dump: {ast.dump(node)}"
        )
