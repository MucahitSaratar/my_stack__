from unicorn import *
from unicorn.arm64_const import *

def read(name):
    with open(name,"rb") as f:
        return f.read()
        
def u32(data):
    return struct.unpack("I", data)[0]
    
def p32(num):
    return struct.pack("I", num)

weOnStackFail = [0x001e6da8]

def hook_code(mu, address, size, user_data):  
    print('>>> Tracing instruction at 0x%x, instruction size = 0x%x' %(address, size))
    if address in weOnStackFail:
        print("Crash Found")
        exit(-11)
    print("> EFLAGS is 0x%x" %(mu.reg_read(UC_ARM64_REG_PSTATE)))
    print("------------------------------------------------")


def forceCrash(error):
    mem_errors = [
            UC_ERR_READ_UNMAPPED, UC_ERR_READ_PROT, UC_ERR_READ_UNALIGNED,
            UC_ERR_WRITE_UNMAPPED, UC_ERR_WRITE_PROT, UC_ERR_WRITE_UNALIGNED,
            UC_ERR_FETCH_UNMAPPED, UC_ERR_FETCH_PROT, UC_ERR_FETCH_UNALIGNED,
        ]
    if uc_error.errno in mem_errors:
            # Memory error - throw SIGSEGV
        os.kill(os.getpid(), signal.SIGSEGV)
    elif uc_error.errno == UC_ERR_INSN_INVALID:
            # Invalid instruction - throw SIGILL
        os.kill(os.getpid(), signal.SIGILL)
    else:
            # Not sure what happened - throw SIGABRT
        os.kill(os.getpid(), signal.SIGABRT)


## Functions 
startaddress = 0x001e6d38
stopaddress = 0x001e6da4


binbase = 0x0
stack_size = 20 * 1024 * 1024
stack_addr = 0x7f000000

mu = Uc(UC_ARCH_ARM64,UC_MODE_ARM)
mu.hook_add(UC_HOOK_CODE, hook_code)

mu.mem_map(binbase,stack_size)
mu.mem_map(stack_addr,stack_size)


mu.mem_write(binbase, read("./binary"))
mu.reg_write(UC_ARM64_REG_SP, stack_addr + stack_size -1)
mu.reg_write(UC_ARM64_REG_X20,0x05)
try:
    mu.emu_start(startaddress,stopaddress)
except UcError as e:
    forceCrash(e)
x20 = mu.reg_read(UC_ARM64_REG_W20)
