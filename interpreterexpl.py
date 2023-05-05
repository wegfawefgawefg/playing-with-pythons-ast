
code -> tokens
tokens -> ast

def basic(a, b, c):
    return a + b + c

def otherthing():
    # all the way to 50
    return 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 + 11 + 12 + 13 + 14 + 15 + 16 + 17 + 18 + 19 + 20 + 21 + 22 + 23 + 24 + 25 + 26 + 27 + 28 + 29 + 30 + 31 + 32 + 33 + 34 + 35 + 36 + 37 + 38 + 39 + 40 + 41 + 42 + 43 + 44 + 45 + 46 + 47 + 48 + 49 + 50

(binop const add (binop const add (binop const add (binop const add const))))


["basic", ["add", "a", "b", "c"]]
ast -> bytecode
vm(bytecode)

'''bytecode ex:'''
# jump to basic

# basic:
#     add a b c

pythonobj -> cstruct, run c code -> copyback to pythonobj





# [Funccallobj(name="basic", args=[Varobj(name="a"), Varobj(name="b"), Varobj(name="c")])

def tokenize(cstring):
    return ["def", "    ", "\t", "\n", "basic", "(", ")", ":", "return", "4", "+", "5"]
def parse(tokens):
    rootnode = Node()
    for token in tokens:
        if token == "def":
            new_node = Nodes.DefNode()
        rootnode.children.append(new_node)

parsertokenizer.tmp