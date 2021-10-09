# context.py  (c)2021  Henrique Moreira
#
# convert sub-string

"""
Show sub-strings to URL using contexts
"""

# pylint: disable=unused-argument


import sys
import ucontext.urlify as urlify


def main():
    """ Main test script! """
    prog = __file__
    code = runner(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print(f"""Usage:

{prog} command [options] string1 [string2 ...]

Commands are:
   url         Show URL with context 'string1'

   youtube     Generate URL from 'Youtube' context

Options are:
   -v          Verbose mode
   -t X        Time string 'X', e.g. t=1h2m3s (1 hour, 2 minute, 3 seconds)
""")
    sys.exit(code if code else 0)


def runner(out, err, args):
    """ Dump file(s) """
    verbose = 0
    time_str = ""
    if not args:
        return None
    cmd = args[0]
    param = args[1:]
    while param and param[0].startswith("-"):
        if param[0] in ("-v", "--verbose"):
            del param[0]
            verbose += 1
            continue
        if param[0] in ("-t", "--time",):
            time_str = param[1]
            del param[:2]
            continue
        return None
    opts = {
        "verbose": verbose,
        "time": time_str,
    }
    if not param:
        return None
    if cmd == "url":
        ctx = param[0]
        del param[0]
        if not param:
            print(f"Use at least one argument after '{cmd} {ctx}'\n")
            return None
        code = context(out, err, ctx, param, opts)
        return code
    if cmd == "youtube":
        code = context(out, err, "youtube", param, opts)
        return code
    return None


def context(out, err, ctx, param, opts) -> int:
    """ Dump URL from context """
    verbose = opts["verbose"]
    time_str = opts["time"]
    if verbose > 0:
        print("Context:", ctx, "; param:", param)
        if time_str:
            print("Time string:", time_str)
    if time_str:
        if not time_str.startswith("t="):
            err.write("Invalid time string: '{time_str}'\n")
    for word in param:
        new = urlify.URL(ctx, word)
        new.add_suffix(time_str)
        out.write(f"{new}\n")
        is_ok = new.is_ok()
        if not is_ok:
            err.write(f"Error in context: '{word}'\n")
            return 1
    return 0


# Main script
if __name__ == "__main__":
    main()
