import sys
import subprocess
import requests
import os

filename = sys.argv[1]
file = open(filename).readlines()

global_includes = []
flags = []

def _compile(flags):
    with open(global_includes[0], "r") as f:
        for l in global_includes:
            fn, fext = os.path.splitext(l)
            if f"#include <{os.path.abspath(fn)}>" not in f.read():
                with open(global_includes[0], "r") as f:
                    contents = f.readlines()

                    if fn != global_includes[0]:
                        contents.insert(0, f"#include <{os.path.abspath(fn)}>")

                with open(global_includes[0], "w") as f:
                    contents = "\n".join(contents)
                    f.write(contents)

    print(f"Transpiling {len(global_includes)} Files into Python...")
    """
    JNS Flags:
        -T: Transpile only (Do not remove after running)
        --workdir: Change Directory
        -C: Compilation Mode (Do not execute)
    """
    print(f"Main File set as {global_includes[0]}")
    subprocess.Popen(["/home/stormedjane/JaneScript/Janescript/jns", os.path.abspath(global_includes[0]),"-C", "-T",]).communicate()
    print("Compiling...")
    res = subprocess.Popen(["pyinstaller", *flags, "outs.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    if res[1]:
        print(res[1].decode())
    elif res[0]:
        print(res[0].decode())
    print("Cleaning up...")
    os.remove("outs.spec")
    print("Finished compilation!")    

for line in file:
    if line.startswith("SET-MAIN"):
        l, fn = line.split()
        if os.path.exists(fn):
            if fn in global_includes:
                global_includes.pop(global_includes.index(fn))
            global_includes.insert(0, fn)
    elif line.startswith("GLOBAL-INCLUDE"):
        for x in line.split()[1:]:
            if "*" in x:
                for l in os.listdir():
                    if l.endswith(os.path.splitext(x)[-1]):
                        global_includes.append(l)
            else:
                if os.path.exists(x):
                    global_includes.append(x)
                else:
                    print(f"Skipping {x} because it has not been found in the current working directory")
    elif line.startswith("COMPILER-FLAGS"):
        f, *flg = line.split()
        flags.extend(flg)
    elif line == "COMPILE":
        _compile(flags)
