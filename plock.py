from sys import argv, stderr
def interpreter(program):
    global stack,ref,pointer,functionMapper
    stack = []
    ref = []
    pointer = 0
    refrer(program)
    runnableProgram = [code(val,i) for i,val in enumerate(program)]
    lexer(runnableProgram)
    while pointer < len(runnableProgram):
        a,*i = runnableProgram[pointer]
        functionMapper[a](*i)
        pointer += 1

def refrer(program):
    global ref
    ref_stack = []
    for i in range(len(program)):
        if program[i] == 'start':
            ref_stack.append(i)
        elif program[i] == 'end':
            ref.append((ref_stack.pop(),i))

def find(num):
    global ref
    for i,j in ref:
        if i == num: return j
        if j == num: return i

stackConsumption ={
'DUMP'  : (-1,1),
'ADD'   : (-1,2),
'SUB'   : (-1,2),
'MULT'  : (-1,2),
'START' : (-1,1),
'END'   : (-1,1),
'DIV'   : (-1,2),
'EQ'    : (-1,2),
'GT'    : (-1,2),
'LT'    : (-1,2),
'MOD'   : (-1,2),
'DUP'   : ( 1,1),
'PUSH'  : ( 1,0),
'SWAP'  : ( 0,2),
'DROP'  : (-1,1),
'OVER'  : ( 1,2), 
}

def lexer(program):
    global stackConsumption
    stack_counter = 0
    for pp,i in enumerate(program):
        x = stackConsumption[i[0]]
        if stack_counter < x[1]:
            stderr.write("ERROR: Trying to read from empty stack at operation {}, {}\n".format(pp, i[0]));
            exit(1)
        stack_counter+=x[0]



#TODO: Convert this to a map
def code(op,pp):
    global functionMapper
    assert len(functionMapper) == 16, "Add the operation to function: code"
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
    elif op == 'swap': return ('SWAP',)
    elif op == 'over': return ('OVER',)
    elif op == 'drop': return ('DROP',)
    else: return ('PUSH',op)


def start(val):
    global stack
    global pointer
    if stack.pop() == 0:
        pointer = val
        
def swap():
    global stack
    (stack[-1] ,stack[-2]) = (stack[-2] , stack[-1])

def over():
    global stack
    stack.append(stack[-2])

def drop():
    global stack
    stack.pop()

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

functionMapper ={
'DUMP'  :dump,
'ADD'   :add,
'SUB'   :sub,
'MULT'  :mult,
'START' :start,
'END'   :end,
'DIV'   :div,
'EQ'    :eq,
'GT'    :gt,
'LT'    :lt,
'MOD'   :mod,
'DUP'   :dup,
'PUSH'  :push,
'SWAP'  :swap,
'DROP'  :drop,
'OVER'  :over
}


stack = []
ref = []
pointer = 0

if __name__ == "__main__":
    if len(argv) < 2:
        stderr.write("ERROR: No argument given\nUSAGE: plock.py <FILENAME>\n")
        exit(1)
    programCode = []
    with open(argv[1]) as f:
        word = f.readlines();
        word = [i.split(sep='//')[0] for i in word]
        for i in word:
            programCode.extend(i.split())
    interpreter(programCode)
