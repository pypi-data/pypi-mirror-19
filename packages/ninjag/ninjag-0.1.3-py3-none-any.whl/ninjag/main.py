import sys
import os
from .core import ninja_generate
from .tk import ioTK
from .io.read import read_config_files


def main(f_out, args):
    if os.path.splitext(f_out)[1] == ".yaml":
        args = [f_out] + args
        f_out = "build.ninja"
        print("output", f_out)
        print(args)
    if len(args) == 0:
        here = os.path.dirname(os.path.realpath(__file__))
        f_usage = os.path.join(here, 'usage.txt')
        print(ioTK.read_all(f_usage))
        print("Error hint: need at least two command line arguments")
        exit()

    ioTK.save_text(
            f_out,
            ninja_generate(read_config_files(args))
        )
