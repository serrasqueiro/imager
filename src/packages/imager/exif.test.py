#-*- coding: utf-8 -*-
# exif.py  (c)2021  Henrique Moreira

"""
Test exif.py (classes for EXIF)
"""

# pylint: disable=missing-function-docstring, unused-argument

import sys
import imager.exif


def main():
    """ Main script.
    """
    code = run_main(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print("""exif.py COMMAND [options] [file(s)]

Commands are:
   show       Display EXIF tags

Options are:
   -v      Verbose
""")
    sys.exit(code if code else 0)


def run_main(out, err, args):
    """ Main run.
    """
    code = None
    if not args:
        return None
    opts = {
        "verbose": 0,
    }
    cmd, param = args[0], args[1:]
    while param and param[0].startswith('-'):
        if param[0] in ("-v", "--verbose"):
            del param[0]
            opts["verbose"] += 1
            continue
        return None
    if cmd == "show":
        code = run_show(out, err, param, opts)
    return code

def run_show(out, err, param:list, opts:dict) -> int:
    """ Show EXIF tags!
    Returns the uggliest error-code for the set of files.
    """
    worse = 0
    assert err
    for fname in param:
        details = len(param) > 1 or opts["verbose"] > 0
        if details:
            print("Image:", fname)
        exifs = imager.exif.hints(fname)
        s_version = "?"
        if exifs:
            s_version = exifs['@version']
            dump_exif(out, fname, exifs, int(details))
        else:
            err.write(f"No exif: {fname}\n")
            if not worse:
                worse = 3
        assert s_version is not None
        if details and exifs:
            print(" " * 4, "Version:", s_version, end="\n\n")
    return worse

def dump_exif(out, fname, exifs, level=0) -> int:
    excl_str = imager.exif.EXCUDE_STR
    simple_tags = ("Copyright", "Description",)
    idx = 0
    for key in sorted(exifs):
        value = exifs[key]
        if value == excl_str:
            continue
        if key.startswith("@"):
            continue
        shown = better_date(value) if key.startswith("Date") else value
        if key in simple_tags:
            simple = shown.strip()
            if not simple:
                continue
        idx += 1
        pre = f"{idx:4} " if level > 0 else ""
        out.write(f"{pre}{key}: {shown}\n")
    return idx

def better_date(value):
    if not isinstance(value, str):
        return value
    return imager.exif.iso_dot_date(value)

# Main script
if __name__ == "__main__":
    main()
