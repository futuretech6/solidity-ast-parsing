import json
import sys


def traverse_node(node):
    if "nodeType" in node:
        if node["nodeType"] == "SourceUnit":
            for node in node["nodes"]:
                traverse_node(node)

        elif node["nodeType"] == "ContractDefinition":
            print(node["name"])
            for node in node["nodes"]:
                traverse_node(node)
                print()

        elif node["nodeType"] == "Block":
            for statement in node["statements"]:
                traverse_node(statement)
                print(";")

        elif node["nodeType"] == "VariableDeclaration":
            print(node["typeDescriptions"]["typeIdentifier"], node["name"])

        elif node["nodeType"] == "FunctionDefinition":
            print(node["name"], "(")
            traverse_node(node["parameters"])
            print(")", "return", "(")
            traverse_node(node["returnParameters"])
            print(")", "{")
            traverse_node(node["body"])
            print("}")

        elif node["nodeType"] == "ParameterList":
            for parameter in node["parameters"]:
                traverse_node(parameter)

        elif node["nodeType"] == "ExpressionStatement":
            traverse_node(node["expression"])

        elif node["nodeType"] == "Identifier":
            print(node["name"])

        elif node["nodeType"] == "Assignment":
            traverse_node(node["leftHandSide"])
            print(node["operator"])
            traverse_node(node["rightHandSide"])

        elif node["nodeType"] == "FunctionCall":
            traverse_node(node["expression"])
            print("(")
            for argument in node["arguments"]:
                traverse_node(argument)
            print(")")

        elif node["nodeType"] == "NewExpression":
            print("new")
            print(node["typeDescriptions"]["typeIdentifier"], "(")
            for argumentType in node["argumentTypes"]:
                print(argumentType["typeIdentifier"])
            print(")")

        elif node["nodeType"] == "ElementaryTypeNameExpression":
            print(node["typeDescriptions"]["typeIdentifier"], "(")
            for argumentType in node["argumentTypes"]:
                print(argumentType["typeIdentifier"])
                print(")")

        elif node["nodeType"] == "IfStatement":
            print("if", "(")
            traverse_node(node["condition"])
            print(")", "{")
            traverse_node(node["trueBody"])
            print("}", "{")
            traverse_node(node["falseBody"])
            print("}")

        elif node["nodeType"] == "BinaryOperation":
            traverse_node(node["leftExpression"])
            print(node["operator"])
            traverse_node(node["rightExpression"])

        elif node["nodeType"] == "MemberAccess":
            traverse_node(node["expression"])
            print(".")
            print(node["memberName"])

        elif node["nodeType"] == "Literal":
            print(node["value"])

        elif node["nodeType"] == "VariableDeclarationStatement":
            print("[")
            for declaration in node["declarations"]:
                traverse_node(declaration)
            print("]", "=")
            traverse_node(node["initialValue"])

        elif node["nodeType"] == "Return":
            print("return")
            traverse_node(node["expression"])

        elif node["nodeType"] == "TupleExpression":
            print("(")
            for component in node["components"]:
                traverse_node(component)
            print(")")

        elif node["nodeType"] == "IndexAccess":
            traverse_node(node["baseExpression"])
            print("[")
            traverse_node(node["indexExpression"])
            print("]")

        else:
            print("[!] Unsupported nodeType {}".format(node["nodeType"]))


help_msg = """
Usage: python main.py <path/to/combined/json>
    Get the combined json by `solc --combined-json ast $file > $combined_json`
"""

if len(sys.argv) <= 1:
    raise RuntimeError("no enough args")
elif len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print(help_msg)
    exit(0)
elif len(sys.argv) == 2:
    combined_json_path = sys.argv[-1]
else:
    raise RuntimeError("too many args")

with open(combined_json_path, "r") as fp:
    combined_json = json.load(fp)

for file, combined in combined_json["sources"].items():
    traverse_node(combined["AST"])
