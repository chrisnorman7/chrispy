from sys import argv
from os import path
import __main__ as main
import file
import functions

if len(argv) == 1:
    file.fname = "temp.txt"
elif len(argv) == 2:
    file.fname = argv[1]
else:
    quit("Syntax: %s [filename]" % argv[0])

if path.isfile(file.fname):
    try:
        f = open(file.fname, "r")
        while True:
            line = f.readline()
            if not line:
                break
            file.contents.append(line)
    except IOError:
        quit("Error opening file: %s." % file.fname)
else:
    print("New file: %s." % file.fname)

print("\n.quit or .exit to quit, .help for help.")

while True:
    line = raw_input("Line %d: " % file.ins)
    if line.startswith("."):
        if line != ".":
            line = line[1:].split(" ")
            func = functions.is_command(line[0])
            if func:
                func(*line[1:])
            else:
                print("%s is not a valid command (.help for help)." % line[0].capitalize())
        else:
            break
    else:
        file.add_line(line)
