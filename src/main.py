import sys
import pathlib
import runpy

root = pathlib.Path(sys.argv[0]).parent
solution = pathlib.Path(sys.argv[1])
module_name = ".".join([*solution.relative_to(root).parent.parts, solution.stem])

if module_name == "main":
    print("Cannot run main.py directly")
    exit(1)

sys.argv = sys.argv[1:]
runpy.run_module(module_name, run_name="__main__")
