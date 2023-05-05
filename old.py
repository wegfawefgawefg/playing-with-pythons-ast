    elif isinstance(node, ast.Call):
        # special case for print
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            return {
                "type": "CallExpression",
                "callee": {"type": "Identifier", "name": "console.log"},
                "arguments": [
                    python_to_js_ast(arg) for arg in node.args
                ]  # # add flags arg
                # + [{"type": }]
            }

        elif isinstance(node.func, ast.Name) and node.func.id == "range":
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