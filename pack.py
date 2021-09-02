#!/bin/python3

"""
Given a path to a python script, recursively resolve all imports and copy
imported modules to a output directory.
"""


import ast
import inspect
import importlib
import os
import sys
from types import ModuleType
import shutil
import re
import stdlib_list

from stdlib_list import stdlib_list

stdlibs = stdlib_list()

PYTHON_DIR = os.path.dirname(sys.executable)


def get_module_relative_component(path: str):
    output = []
    for p in sys.path:
        if path.startswith(p):
            output.append(path.removeprefix(p).removeprefix("/"))
    output.sort(key=len)
    if len(output) > 0:
        return output[0]


_STDLIB_PATH_PATTERN = re.compile(r"lib/[Pp]ython[2-9]\.\d+$")


def is_stdlib_module(module):
    return module.__name__ in stdlibs or \
        PYTHON_DIR in module.__file__ or \
        _STDLIB_PATH_PATTERN.search(os.path.dirname(module.__file__))


def enumerate_modules(module, visited=None):
    if visited is None:
        yield module.__name__, module.__file__, os.path.basename(module.__file__)
        visited = set()
    # Process direct imports like
    # import abc
    # or
    # from module1 import module2
    # note if module2 is a function, the loop below won't process it.
    if is_stdlib_module(module):
        return
    for (k, v) in list(module.__dict__.items()):
        if isinstance(v, ModuleType) and hasattr(v, '__file__'):
            if is_stdlib_module(v):
                continue
            if v not in visited:
                visited.add(v)
                yield v.__name__, v.__file__, get_module_relative_component(v.__file__)
                yield from enumerate_modules(v, visited)
    # Process imports like
    # from module1 import module2
    # in this case we want to list module1 as a dependency as well
    try:
        source = inspect.getsource(module)
    except OSError:
        return
    module_ast = ast.parse(source)
    from_imports: list[ast.ImportFrom] = [
        node for node in ast.walk(module_ast)
        if isinstance(node, ast.ImportFrom)
    ]
    relative_root = module.__name__
    if hasattr(module, '__package__'):
        relative_root = module.__package__
    for node in from_imports:
        if node.module is None:
            continue
        try:
            v = importlib.import_module(
                "."*node.level + node.module, relative_root)
        except ModuleNotFoundError:
            print("Module", node.module, "in",
                  relative_root, "not found, ignored")
            continue
        except Exception as e:
            print("Module", node.module, "import failed due to", e, "ignored")
            continue
        if not hasattr(v, '__file__'):
            continue
        if is_stdlib_module(v):
            continue
        if v not in visited:
            visited.add(v)
            yield v.__name__, v.__file__, get_module_relative_component(v.__file__)
            yield from enumerate_modules(v, visited)


def print_usage(argv):
    print("Usage:", argv[0], "some_python_script.py <output dir>")


def main(argv):
    if len(argv) != 3:
        print_usage(argv)
        return 1
    path = argv[1]
    output_dir = argv[2]
    os.makedirs(output_dir, exist_ok=True)
    # spec = importlib.util.spec_from_file_location(path, path)
    # module = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(module)
    import web_server_flask as module
    for (name, path, relative_path) in enumerate_modules(module):
        target_path = os.path.join(output_dir, relative_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copy(path, target_path)
        print(name, path, relative_path)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
