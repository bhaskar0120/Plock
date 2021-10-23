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
'DUMP'      : (-1,1),
'ADD'       : (-1,2),
'SUB'       : (-1,2),
'MULT'      : (-1,2),
'START'     : (-1,1),
'END'       : (-1,1),
'DIV'       : (-1,2),
'EQ'        : (-1,2),
'GT'        : (-1,2),
'LT'        : (-1,2),
'MOD'       : (-1,2),
'DUP'       : ( 1,1),
'PUSH'      : ( 1,0),
'SWAP'      : ( 0,2),
'DROP'      : (-1,1),
'OVER'      : ( 1,2), 
'NOT'       : ( 0,1),
'AND'       : (-1,2),
'OR'        : (-1,2),
'SHL'       : (-1,2),
'SHR'       : (-1,2),
'MEM'       : ( 1,0),
'READ8'     : ( 0,1),
'WRITE8'    : (-2,2),
'READ16'    : ( 0,1),
'WRITE16'   : (-2,2),
'READ32'    : ( 0,1),
'WRITE32'   : (-2,2),
'READ64'    : ( 0,1),
'WRITE64'   : (-2,2),
'PUTS'      : ( 0,1),
'PRINTF'    : ( 0,1),
'SCANF'     : ( 0,1),
'PUSHSTR'   : ( 1,0),
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
    assert 34 == len(stackConsumption), "Discrepancy in function: code"
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
    elif op == 'read8' : return ('READ8',)
    elif op == 'write8' : return ('WRITE8',)
    elif op == 'read16' : return ('READ16',)
    elif op == 'write16' : return ('WRITE16',)
    elif op == 'read32' : return ('READ32',)
    elif op == 'write32' : return ('WRITE32',)
    elif op == 'read64' : return ('READ64',)
    elif op == 'write64' : return ('WRITE64',)
    elif op == 'puts' : return ('PUTS',)
    elif op == 'printf' : return ('PRINTF',)
    elif op == 'scanf' : return ('SCANF',)
    elif op == '<<' : return('SHL',)
    elif op == '>>' : return('SHR',)
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
    x.append(0x00)
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

def write8():
    global stack, memory
    a = stack.pop()
    memory[stack.pop()] = a

def write16():
    global stack, memory
    a = stack.pop()
    b = stack.pop()
    for i,val in enumerate(a.to_bytes(2,'big')):
        memory[b+i] =val

def write32():
    global stack, memory
    a = stack.pop()
    b = stack.pop()
    for i,val in enumerate(a.to_bytes(4,'big')):
        memory[b+i] =val

def write64():
    global stack, memory
    a = stack.pop()
    b = stack.pop()
    for i,val in enumerate(a.to_bytes(8,'big')):
        memory[b+i] =val

def read8():
    global stack, memory
    stack.append(memory[stack.pop()])

def read16():
    global stack, memory
    a = stack.pop()
    stack.append(int.from_bytes(memory[a:a+2],'big'))

def read32():
    global stack, memory
    a = stack.pop()
    stack.append(int.from_bytes(memory[a:a+4],'big'))

def read64():
    global stack, memory
    a = stack.pop()
    stack.append(int.from_bytes(memory[a:a+8],'big'))

def shl():
    global stack
    a = stack.pop()
    stack[-1] = stack[-1] << a

def shr():
    global stack
    a = stack.pop()
    stack[-1] = stack[-1] >> a

#Switch these to external functions
def printf():
    a = stack.pop()
    x = memory[a]
    buf = []
    while not x == 0:
        buf.append(chr(x))
        a += 1
        x = memory[a]
    print(''.join(buf),end="")
    stack.append(len(buff))

def puts():
    a = stack.pop()
    x = memory[a]
    buf = []
    while not x == 0:
        buf.append(chr(x))
        a += 1
        x = memory[a]
    print(''.join(buf))
    stack.append(len(buf)+1)

def scanf():
    pass

functionMapper ={
'DUMP'      :dump,
'ADD'       :add,
'SUB'       :sub,
'MULT'      :mult,
'START'     :start,
'END'       :end,
'DIV'       :div,
'EQ'        :eq,
'GT'        :gt,
'LT'        :lt,
'MOD'       :mod,
'DUP'       :dup,
'PUSH'      :push,
'SWAP'      :swap,
'DROP'      :drop,
'OVER'      :over,
'NOT'       :Not,
'AND'       :And,
'OR'        :Or,
'MEM'       :mem,
'WRITE8'    :write8,
'READ8'     :read8,
'WRITE16'   :write16,
'READ16'    :read16,
'WRITE32'   :write32,
'READ32'    :read32,
'WRITE64'   :write64,
'READ64'    :read64,
'PUSHSTR'   :pushstr,
'PUTS'      :puts,
'PRINTF'    :printf,
'SCANF'     :scanf,
'SHL'       :shl,
'SHR'       :shr,
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
    
