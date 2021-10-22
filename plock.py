from sys import argv, stderr
def interpreter():
    global stack,ref,pointer,functionMapper,program
    stack = []
    ref = []
    pointer = 0
    refrer()
    runnableProgram = [code(val,i) for i,val in enumerate(program)]
    stack_strict(runnableProgram)
    while pointer < len(runnableProgram):
        a,*i = runnableProgram[pointer]
        functionMapper[a](*i)
        pointer += 1

def refrer():
    global ref, program
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

def lexer_file(programFile):
    global program
    try:
        word = []
        with open(programFile) as f:
            word = f.readlines()
        word = [i.split(sep="//")[0] for i in word]
        for i,val in enumerate(word):
            quote_count = val.count('"')
            if not quote_count % 2 == 0:
                stderr.write("ERROR: Missing quotation mark at line {}\n".format(i+1))
                exit(1)
        programCode = []
        for i in word:
            programCode.extend(i.split())
        adding_stack = []
        add_to_stack = False
        for i in programCode:
            adding_stack.append(i)
            if i.count('"') == 1:
                add_to_stack = not add_to_stack
            if not add_to_stack:
                program.append(' '.join(adding_stack))
                adding_stack.clear()
    except FileNotFoundError:
        stderr.write("ERROR: Specified File not found {}\n".format(programFile))
        exit(1)

stackConsumption ={
'DUMP'    : (-1,1),
'ADD'     : (-1,2),
'SUB'     : (-1,2),
'MULT'    : (-1,2),
'START'   : (-1,1),
'END'     : (-1,1),
'DIV'     : (-1,2),
'EQ'      : (-1,2),
'GT'      : (-1,2),
'LT'      : (-1,2),
'MOD'     : (-1,2),
'DUP'     : ( 1,1),
'PUSH'    : ( 1,0),
'SWAP'    : ( 0,2),
'DROP'    : (-1,1),
'OVER'    : ( 1,2), 
'NOT'     : ( 0,1),
'AND'     : (-1,2),
'OR'      : (-1,2),
'MEM'     : ( 1,0),
'READ'    : ( 0,1),
'WRITE'   : (-2,2),
'PUSHSTR' : ( 1,0),
}

def stack_strict(program):
    global stackConsumption
    stack_counter = 0
    for pp,i in enumerate(program):
        x = stackConsumption[i[0]]
        if stack_counter < x[1]:
            stderr.write("ERROR: Trying to read from empty stack at operation {}, {}\n".format(pp, i[0]))
            exit(1)
        stack_counter+=x[0]



#TODO: Convert this to a map
def code(op,pp):
    global functionMapper
#Development Only ----------------------
    global stackConsumption
    assert 23 == len(stackConsumption), "Discrepancy in function: code"
#---------------------------------------
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
    elif op == '!' : return ('NOT',)
    elif op == '&' : return ('AND',)
    elif op == '|' : return ('OR',)
    elif op == 'mem' : return ('MEM',)
    elif op == 'read' : return ('READ',)
    elif op == 'write' : return ('WRITE',)
    elif op[0] == '"' : return ('PUSHSTR',op[1:-1])
    else:
        try: 
            x = int(op)
            return ('PUSH',x)
        except ValueError:
            stderr.write("ERROR: Unknown instruction {} at instruction number {}\n".format(op,pp))
            exit(1)


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
    stack.append(val)

def pushstr(val):
    global stack,memory
    x = bytearray(val,'utf-8')
    stack.append(len(memory))
    memory.extend(x)
    

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

def Not():
    global stack
    stack[-1] = int(not stack[-1])

def And():
    global stack
    a = stack.pop()
    stack[-1] &= a 

def Or():
    global stack
    a = stack.pop()
    stack[-1] |= a

def div():
    global stack
    a = stack.pop()
    stack.append(stack.pop()//a)

def mult():
    global stack
    stack.append(stack.pop()*stack.pop())

def sub():
    global stack
    a = stack.pop()
    stack.append(stack.pop()-a)

def add():
    global stack
    stack.append(stack.pop()+stack.pop())

def mem():
    global stack
    stack.append(0) #Hard coded for now, must change in compilation mode

def write():
    global stack, memory
    a = stack.pop()
    memory[stack.pop()] = a

def read():
    global stack, memory
    stack.append(memory[stack.pop()])

functionMapper ={
'DUMP'    :dump,
'ADD'     :add,
'SUB'     :sub,
'MULT'    :mult,
'START'   :start,
'END'     :end,
'DIV'     :div,
'EQ'      :eq,
'GT'      :gt,
'LT'      :lt,
'MOD'     :mod,
'DUP'     :dup,
'PUSH'    :push,
'SWAP'    :swap,
'DROP'    :drop,
'OVER'    :over,
'NOT'     :Not,
'AND'     :And,
'OR'      :Or,
'MEM'     :mem,
'WRITE'   :write,
'READ'    :read,
'PUSHSTR' :pushstr,
}


stack = []
ref = []
pointer = 0
MAX_MEMORY = 64000
memory = bytearray(MAX_MEMORY)
program = []

            

if __name__ == "__main__":
    if len(argv) < 2:
        stderr.write("ERROR: No argument given\nUSAGE: plock.py <FILENAME>\n")
        exit(1)
    lexer_file(argv[1])
    #Development only
    assert len(functionMapper) == len(stackConsumption), "Discrepancy in functionMapper"
    assert len(stackConsumption) == len(stackConsumption), "Discrepancy in  stackConsumption"
    interpreter()
    
