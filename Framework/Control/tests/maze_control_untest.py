import maze_control_support
from maze_control_support import control
from maze_control import destroy_Toplevel1, create_Toplevel1
import unittest
import pytest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


class TestFrameworkControl(unittest.TestCase):

    def test_init_ui(self):
        root = tk.Tk()
        maze_control_support.set_Tk_var()
        create_Toplevel1(root)
        destroy_Toplevel1()
