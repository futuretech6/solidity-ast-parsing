import json
import sys


def traverse_node(node, action: str = "print"):
    if "nodeType" in node:
        if node["nodeType"] == "SourceUnit":
            for node in node["nodes"]:
                traverse_node(node, action)

        elif node["nodeType"] == "PragmaDirective":
            print("pragma", *node["literals"], ";")

        elif node["nodeType"] == "ContractDefinition":
            print("contract", node["name"], "{")
            for node in node["nodes"]:
                traverse_node(node, action)
                print()
            print("}")

        elif node["nodeType"] == "Block":
            for statement in node["statements"]:
                traverse_node(statement, action)
                print(";")

        elif node["nodeType"] == "VariableDeclaration":
            print(
                node["typeDescriptions"]["typeString" if action == "print" else "typeIdentifier"],
                node["name"],
                ";" if node["stateVariable"] else "",
            )

        elif node["nodeType"] == "FunctionDefinition":
            print("function", node["name"], "(")
            traverse_node(node["parameters"], action)
            print(")", "returns", "(")
            traverse_node(node["returnParameters"], action)
            print(")", "{")
            traverse_node(node["body"], action)
            print("}")

        elif node["nodeType"] == "ParameterList":
            isFirst = True
            for parameter in node["parameters"]:
                if not isFirst:
                    print(",")
                isFirst = False
                traverse_node(parameter, action)

        elif node["nodeType"] == "ExpressionStatement":
            traverse_node(node["expression"], action)

        elif node["nodeType"] == "Identifier":
            print(node["name"])

        elif node["nodeType"] == "Assignment":
            traverse_node(node["leftHandSide"], action)
            print(node["operator"])
            traverse_node(node["rightHandSide"], action)

        elif node["nodeType"] == "FunctionCall":
            traverse_node(node["expression"], action)
            print("(")
            for argument in node["arguments"]:
                traverse_node(argument, action)
            print(")")

        elif node["nodeType"] == "NewExpression":
            print("new")
            print(node["typeDescriptions"]["typeString" if action == "print" else "typeIdentifier"], "(")
            for argumentType in node["argumentTypes"]:
                print(argumentType["typeString" if action == "print" else "typeIdentifier"])
            print(")")

        elif node["nodeType"] == "ElementaryTypeNameExpression":
            print(node["typeDescriptions"]["typeString" if action == "print" else "typeIdentifier"])
            # print("(")
            # for argumentType in node["argumentTypes"]:
            #     print(argumentType["typeString" if action == "print" else "typeIdentifier"])
            #     print(")")

        elif node["nodeType"] == "IfStatement":
            print("if", "(")
            traverse_node(node["condition"], action)
            print(")", "{")
            traverse_node(node["trueBody"], action)
            print("}", "{")
            traverse_node(node["falseBody"], action)
            print("}")

        elif node["nodeType"] == "BinaryOperation":
            traverse_node(node["leftExpression"], action)
            print(node["operator"])
            traverse_node(node["rightExpression"], action)

        elif node["nodeType"] == "MemberAccess":
            traverse_node(node["expression"], action)
            print(".")
            print(node["memberName"])

        elif node["nodeType"] == "Literal":
            print(node["value"])

        elif node["nodeType"] == "VariableDeclarationStatement":
            print("(")
            isFirst = True
            for declaration in node["declarations"]:
                if not isFirst:
                    print(",")
                isFirst = False
                traverse_node(declaration, action)
            print(")", "=")
            traverse_node(node["initialValue"], action)

        elif node["nodeType"] == "Return":
            print("return")
            traverse_node(node["expression"], action)

        elif node["nodeType"] == "TupleExpression":
            print("(")
            isFirst = True
            for component in node["components"]:
                if not isFirst:
                    print(",")
                isFirst = False
                traverse_node(component, action)
            print(")")

        elif node["nodeType"] == "IndexAccess":
            traverse_node(node["baseExpression"], action)
            print("[")
            traverse_node(node["indexExpression"], action)
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
