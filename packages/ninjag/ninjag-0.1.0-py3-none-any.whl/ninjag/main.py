import yaml
import sys
from .core import ninja_generate
from .check_input import check_input


def main(f_out, args):
    output = []
    for f in args:
        with open(f, "r") as IN:
            output.append(
                ninja_generate(
                    check_input(yaml.load(IN.read()))
                    )
                )
    with open(f_out, 'w') as OUT:
        OUT.write("\n".join(output) + "\n")
