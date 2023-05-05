import escodegen

js_ast = {
    "type": "Program",
    "body": [
        {
            "type": "CallExpression",
            "callee": {"type": "Identifier", "name": "console.log"},
            "arguments": [{"type": "Literal", "value": 1}],
        }
    ],
}

larger_ast = {
    "type": "Program",
    "body": [
        {
            "type": "FunctionDeclaration",
            "id": {"type": "Identifier", "name": "printtest"},
            "params": [],
            "body": {
                "type": "BlockStatement",
                "body": [
                    {
                        "type": "CallExpression",
                        "callee": {"type": "Identifier", "name": "console.log"},
                        "arguments": [{"type": "Literal", "value": 1}],
                    }
                ],
            },
        }
    ],
}

escodegen.generate(js_ast)
