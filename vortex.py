from pwn import log, remote, context
from pwnlib.util.packing import p32, u32

def main():

    p = remote('vortex.labs.overthewire.org', 5842)
    # context.log_level = 'debug'
    context.endianness = 'little'

    total = 0

    for i in range(4):
        readin = u32(p.recv(numb = 4))
        total += readin

    log.info(f'{total=}')

    p.sendline(p32(int(total)))
    try:
        server_response = p.recvall()
        log.info(f'{server_response=}')
    except:
        log.info('Error')

    p.close()

if __name__ == '__main__':

    main()
