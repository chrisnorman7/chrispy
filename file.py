contents, line, fname = [], "", ""

ins = len(contents) + 1

def file_end():
    return len(contents) + 1

def add_line(line):
    global ins, contents
    contents.insert(ins, line)
    ins += 1
