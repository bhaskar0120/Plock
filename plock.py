from sys import argv
def interpreter(program):
    global stack,ref,pointer
    stack = []
    ref = []
    pointer = 0
    refrer(program)
    runnableProgram = [code(val,i) for i,val in enumerate(program)]
    while pointer < len(runnableProgram):
        a,*i = runnableProgram[pointer]
        functionMapper[a](*i)
        pointer += 1

def refrer(program):
    global ref
    for i in range(len(program)):
        if program[i] == 'start':
            stack.append(i)
        elif program[i] == 'end':
            ref.append((stack.pop(),i))

def find(num):
    global ref
    for i,j in ref:
        if i == num: return j
        if j == num: return i

def code(op,pp):
    if op == "." : return ('DUMP',)
    elif op == '+' : return ('ADD',)
    elif op == '-' :return ('SUB',)
    elif op == '*' : return ('MULT',)
    elif op == 'start' : return ('START',find(pp))
    elif op == 'end' :  return ('END',find(pp))
    elif op == '/' : return ('DIV',)
    elif op == '==' : return ('EQ',)
    elif op == '>' : return ('GT',)
    elif op == '<' : return ('LT',)
    elif op == '%': return ('MOD',)
    elif op == 'dup' : return ('DUP',)
    else: return ('PUSH',op)



def start(val):
    global stack
    global pointer
    if stack.pop() == 0:
        pointer = val
        
def mod():
    global stack
    a= stack.pop()
    stack.append(stack.pop()%a)

def dup():
    global stack
    stack.append(stack[-1])

def end(val):
    global stack, pointer
    if stack.pop() == 0:
        pointer = val
        
def push(val):
    global stack
    stack.append(int(val))

def dump():
    global stack
    print(stack.pop())

def gt():
    global stack
    if stack.pop() < stack.pop() : stack.append(1)
    else: stack.append(0)

def lt():
    global stack
    if stack.pop() > stack.pop() : stack.append(1)
    else: stack.append(0)

def eq():
    global stack
    if stack.pop() == stack.pop(): stack.append(1)
    else: stack.append(0)

def div():
    global stack
    a = stack.pop()
    stack.append(stack.pop()//a)

def mult():
    global stack
    stack.append(stack.pop()*stack.pop())

def sub():
    global stack
    a = stack.pop();
    stack.append(stack.pop()-a)

def add():
    global stack
    stack.append(stack.pop()+stack.pop())

functionMapper = {}
functionMapper['DUMP'] = dump
functionMapper['ADD'] = add
functionMapper['SUB'] = sub
functionMapper['MULT'] = mult
functionMapper['START'] = start
functionMapper['END'] = end
functionMapper['DIV'] = div
functionMapper['EQ'] = eq
functionMapper['GT'] = gt
functionMapper['LT'] = lt
functionMapper['MOD'] = mod
functionMapper['DUP'] = dup
functionMapper['PUSH'] = push

stack = []
ref = []
pointer = 0
if __name__ == "__main__":
    if len(argv) < 2:
        print("ERROR: No argument given\nUSAGE: plock.py <FILENAME>")
        exit(1)
    programCode = []
    with open(argv[1]) as f:
        word = f.readlines();
        word = [i.split(sep='//')[0] for i in word]
        for i in word:
            programCode.extend(i.split())
    interpreter(programCode)
