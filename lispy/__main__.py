import sys
import lispy
from lispy import Repl
from lispy.io import execute_file

if len(sys.argv) == 2:
    execute_file(sys.argv[1])
else:
    Repl().repl()
