"""
Ninjag: Ninja build file generator

Usage: ninjag output.ninja in1.yaml in2.yaml ...
Author: Steven(Yuhang) Wang
License: MIT/X11
"""
import sys
from .main import main


def cli():
    main(sys.argv[1], sys.argv[2:])
