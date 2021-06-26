import sys, getopt
import pyglet


global winwidth
global winheight

global inputfile
inputfile = ""

l, p = getopt.getopt(sys.argv[1:], "i:", ["input="])
for o, a in l:
    if o in ["i", "--input"]:
        inputfile = a

if inputfile == "":
    print("No input file found! (please pass the --input parameter)")
    sys.exit(1)

x = open(inputfile, "r")
y = x.readlines()

tape = [0]
tape_head = 0
looping = False
start_pos = []
end_pos = []
instructions_pointer = 0
com_num = 0
ln_num = 0
windowActive = False
hasbeenon = True

elements = [pyglet.text]

window = pyglet.window.Window(width=winwidth, height=winheight)

# remove newline characters from lists, so that they aren't parsed. ####################################################

for i in y:
    c = i
    i = list(i)
    if i[len(i) - 1] == "\n":
        i.remove("\n")
    i = "".join(i)
    y[y.index(c)] = i
    com_num += 1

strins = " ".join(y)
# print(strins, instructions_pointer, "\n")


# time to parse the brain f ############################################################################################

def cmd_add():
    tape[tape_head] += 1
    if tape[tape_head] > 255:
        tape[tape_head] = 0


def cmd_sub():
    tape[tape_head] -= 1
    if tape[tape_head] <= -1:
        tape[tape_head] = 255


def cmd_right():
    global tape_head
    tape_head += 1
    if tape_head >= len(tape):
        tape.append(0)


def cmd_left():
    global tape_head
    tape_head -= 1
    if tape_head < 0:
        tape.insert(0, 0)
        tape_head = 0


def cmd_if_not_zero():
    global tape_head
    global start_pos
    global instructions_pointer
    if tape[tape_head] != 0:
        start_pos.append(instructions_pointer)

    else:
        instructions_pointer = end_pos.pop()


def cmd_end_loop():
    global tape_head
    global start_pos
    global instructions_pointer
    end_pos.append(instructions_pointer)
    instructions_pointer = start_pos.pop() - 1


def cmd_in():
    global tape_head
    tmp = sys.stdin.read(1)
    tape[tape_head] = ord(tmp)


def cmd_print():
    global windowActive
    if tape[tape_head] < 128:
        print(chr(tape[tape_head]), end="")

    if tape[tape_head] == 129:
        hasbeenon = False


def cmd_print_val():
    print(str(tape[tape_head]), end="")



funcs = {
    "+": cmd_add,
    "-": cmd_sub,
    ">": cmd_right,
    "<": cmd_left,
    "[": cmd_if_not_zero,
    "]": cmd_end_loop,
    ".": cmd_print,
    ",": cmd_in,
    "^": cmd_print_val
}


while instructions_pointer < len(strins):
    cmd = strins[instructions_pointer]
    # print("%s:%d" % (cmd, instructions_pointer))

    if cmd in funcs.keys():
        funcs[cmd]()

    if not hasbeenon:
        pyglet.app.run()
        hasbeenon = True


def on_draw():
    window.clear()
    for k in elements:
        k.draw()

    if not windowActive:
        window.close()



    # print(tape, tape_head, cmd)
    # print(start_pos)

    instructions_pointer += 1

# debug output #########################################################################################################
"""
for e in y:
    print(e)
"""
