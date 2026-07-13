"""Recover Python source from .pyc bytecode (Python 3.13)"""
import dis, marshal, sys, types, os, glob, importlib.util

BACKEND = r"C:\Users\yashb\OneDrive\Desktop\opencode-second-brain\backend"

def dis_file(pyc_path):
    """Extract readable info from a .pyc file"""
    with open(pyc_path, 'rb') as f:
        f.read(16)  # skip header (Python 3.13 = 16 bytes)
        code = marshal.load(f)

    print(f"\n{'='*60}")
    print(f"FILE: {pyc_path}")
    print(f"{'='*60}")
    print(f"Name: {code.co_name}")
    print(f"Constants ({len(code.co_consts)}):")
    for c in code.co_consts:
        if isinstance(c, str) and len(c) > 0:
            print(f"  STR: {repr(c)[:120]}")
        elif isinstance(c, types.CodeType):
            print(f"  FUNC: {c.co_name}({c.co_varnames[:c.co_argcount]})")
        elif isinstance(c, int) and c > 100:
            print(f"  INT: {c}")
        elif isinstance(c, float):
            print(f"  FLOAT: {c}")

    print(f"Names ({len(code.co_names)}):")
    for n in code.co_names:
        print(f"  {n}")

    print(f"Varnames ({len(code.co_varnames)}):")
    for v in code.co_varnames:
        print(f"  {v}")

    # Recurse into function constants
    for c in code.co_consts:
        if isinstance(c, types.CodeType):
            print(f"\n  --- Function: {c.co_name} ---")
            print(f"  Varnames: {list(c.co_varnames[:c.co_argcount])}")
            for cc in c.co_consts:
                if isinstance(cc, str) and len(cc) > 0:
                    print(f"    STR: {repr(cc)[:120]}")
            for n in c.co_names:
                print(f"    NAME: {n}")

# Find all .pyc files
pyc_files = []
for root, dirs, files in os.walk(BACKEND):
    for f in files:
        if f.endswith('.pyc'):
            pyc_files.append(os.path.join(root, f))

for pf in sorted(pyc_files):
    try:
        dis_file(pf)
    except Exception as e:
        print(f"\nERROR on {pf}: {e}")