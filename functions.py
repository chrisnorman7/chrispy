from inspect import getdoc, getargspec
import __main__ as main
import file
from time import gmtime, time

start, current = 0, gmtime()

commands = {}

def parse_range(spec):
    if not spec:
        spec = [1, file.file_end()]
    else:
        if spec.find(":"):
            spec = spec.split(":")
        else:
            try:
                spec = [int(spec),""]
            except ValueError:
                print("Valid ranges are written as from:to, where from and to are line numbers starting at 1, and not exceding the length of the currently loaded file. Either from or to can be ommited")
                return 0
        if not spec[0]:
            spec[0] = 1
        if not spec[1]:
            spec[1] = file.file_end()
        for i in range(2):
            try:
                spec[i] = int(spec[i])
            except ValueError:
                print("Not a number: %r." % spec[i])
                return 0
        if spec[0] < 1:
            print("Error: %d less than 1." % spec[0])
            return 0
        elif spec[1] > file.file_end():
            print("Error: %d would put your cursor past the end of the file." % spec[1])
            return 0
        elif spec[0] > spec[1]:
            print("Reverse range: %d:%d." % (spec[0], spec[1]))
            return 0
    return spec

def register_command(command, function): commands[command] = function

def do_list(range_spec = 0):
    """
This command lists the contents of the current file according to the supplied range. Line numbers are also printed.
    """
    range_spec = parse_range(range_spec)
    range_spec[1] -= 1
    if range:
        for c in range(*range_spec):
            print("%d: %s" % (c, file.contents[c][0:-1]))

def do_print(range = 0):
    """
    This command prints either the specified range, or the contents of the file without line numbers.
    """
    for line in file.contents:
        print(line[0:-1])

def exit():
    """
This command quits the editor, saving the file you have been working on.
    """
    if file.contents:
        f = open(file.fname, "w")
        for line in file.contents:
            f.write("%s\n" % line)
        f.close()
        print("Saving changes to disk.")
    else:
        print("No changes to save.")
    quit("Exiting.")

def do_help(cmd = "help"):
    """
This command gives you help with all other commands.

For example:
help quit
Will give you usage instructions for the quit command.
    """
    real_func = is_command(cmd)
    if real_func:
        print("Showing help on command %s:\n\n%s" % (cmd, getdoc(real_func)))
        return 1
    else:
        print("No function named %s." % cmd)
        return 0

def is_command(func):
    try:
        return commands[func]
    except KeyError:
        return False
    
def parseFunction(func, **args):
    spec = getargspec(func)
    if len(args) > len(spec[0]):
        print("Too many arguments. Max is %d." % len(spec[0]))
    elif len(args) < len(spec[3]):
        print("Not enough arguments. Minimum is %d." % len(spec[3]))
    else:
        return func(args)
    return 0

def timer():
    """
    This command sets and clears the Samaritans timer.
    Usage:
    
    .timer the first time starts the timer. The same command when you have finished the call will stop it again.
    """
    global start, current
    if start:
        text = "%d:%d-%d" % (current.tm_hour, current.tm_min, (int(time()) - start) / 60)
        print(text)
        file.add_line(text)
        start = 0
    else:
        start = int(time())
        current = gmtime(start)
        print("Started call at %d:%d." % (current.tm_hour, current.tm_min))

register_command("list", do_list)
register_command("print", do_print)
register_command("exit", exit)
register_command("quit", exit)
register_command("help", do_help)
register_command("time", timer)
