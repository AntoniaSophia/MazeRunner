# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import build.cmake_example as m


def test_main():
    assert m.__version__ == "dev"
    assert m.add(1, 2) == 3
    assert m.subtract(1, 2) == -1
