import sys
import re
from lark import Lark, Transformer, v_args, UnexpectedInput
import yaml

grammar = r"""
    start: (statement)*

    ?statement: assignment
              | dict_or_array
              | COMMENT

    assignment: NAME ":=" value

    dict_or_array: value

    ?value: number
          | array
          | dict
          | const_ref

    number: SIGNED_FLOAT
    array: "#(" (value ("," value)*)? ")"
    dict: "{" [pair ("," pair)*] "}"
    pair: NAME ":" value

    const_ref: "$" NAME "$"

    COMMENT: "'" /[^\n]*/

    %import common.SIGNED_FLOAT
    %import common.CNAME -> NAME
    %import common.WS
    %ignore WS
    %ignore COMMENT
"""

parser = Lark(grammar, parser='lalr')

class ConfigTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.constants = {}

    def start(self, items):
        result = []
        for item in items:
            if isinstance(item, dict) or isinstance(item, list):
                result.append(item)
        if len(result) == 1:
            return result[0]
        elif len(result) > 1:
            return result
        else:
            return {}

    def assignment(self, args):
        name, val = args
        self.constants[name] = val
        return None

    def NAME(self, token):
        return str(token)

    def number(self, args):
        num_str = str(args[0])
        if '.' in num_str:
            return float(num_str)
        else:
            return int(num_str)

    def array(self, items):
        return list(items)

    def dict(self, pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError(f"Duplicate key '{k}' in dictionary")
            d[k] = v
        return d

    def pair(self, args):
        return (args[0], args[1])

    def const_ref(self, args):
        name = args[0]
        if name not in self.constants:
            raise NameError(f"Undefined constant: {name}")
        return self.constants[name]

def main():
    try:
        text = sys.stdin.read()
        tree = parser.parse(text)
        transformer = ConfigTransformer()
        result = transformer.transform(tree)
        yaml.dump(result, sys.stdout, allow_unicode=True, sort_keys=False)
    except UnexpectedInput as e:
        print(f"Syntax error at line {e.line}, column {e.column}: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, NameError) as e:
        print(f"Semantic error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

