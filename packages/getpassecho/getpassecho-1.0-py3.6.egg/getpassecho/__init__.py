import sys
import os
import sys
import termios
import fcntl


def getch():
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        while 1:
            try:
                c = sys.stdin.read(1)
                break
            except IOError:
                pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    return c


def getpass(prompt=None, stream=None, echo=True, echo_char='*'):
    if stream is None:
        stream = sys.stdout
    if prompt is None:
        prompt = 'Password: '

    stream.write(prompt)
    passwd = ''
    c = None
    while True:
        c = getch()
        if c == '\n':
            break
        passwd += c
        if echo:
            sys.stdout.write(echo_char)
    return passwd
