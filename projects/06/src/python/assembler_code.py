"""Code module of the Assembler"""


def dest(command: str) -> str:
    """Return the binary code of the 'dest' part of a C-Command.

    Input must be a well-formed C-Command.
    """
    if '=' not in command:
        return '000'

    a = '0'
    d = '0'
    m = '0'

    dest_mnem = command.split('=', 1)[0]

    for dest in dest_mnem:
        if dest == 'A':
            a = '1'
        if dest == 'D':
            d = '1'
        if dest == 'M':
            m = '1'

    return a + d + m


COMP_MNEM_BINARY_MAP = {
    '0': '101010',
    '1': '111111',
    '-1': '111010',
    'D': '001100',
    'A': '110000',
    '!D': '001101',
    '!A': '110001',
    '-D': '001111',
    '-A': '110001',
    'D+1': '011111',
    'A+1': '110111',
    'D-1': '001110',
    'A-1': '110010',
    'D+A': '000010',
    'D-A': '010011',
    'A-D': '000111',
    'D&A': '000000',
    'D|A': '010101',
}


def comp(command: str) -> str:
    """Return the binary code of the 'comp' part of a C-Command.

    Input must be a well-formed C-Command.
    """
    comp = command.split('=', 1)[1] if '=' in command else command.split(';', 1)[0]
    return COMP_MNEM_BINARY_MAP[comp]


JUMP_MNEM_BINARY_MAP = {
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}


def jump(command: str) -> str:
    """Return the binary code of the 'jump' part of a C-Command

    Input must be a well-formed C-Command.
    """
    if ';' not in command:
        return '000'

    comp = command.split(';', 1)[1]
    return JUMP_MNEM_BINARY_MAP[comp]
