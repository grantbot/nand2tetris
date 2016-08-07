"""Code module of the Assembler"""

DEST_MNEM_BINARY_MAP = {
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111',
}


def dest(dest_mnem: str) -> str:
    """Return the binary code of the 'dest' part of a C-Command"""
    if dest_mnem:
        return DEST_MNEM_BINARY_MAP[dest_mnem]
    return '000'

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


def comp(comp_mnem: str) -> str:
    """Return the binary code of the 'comp' part of a C-Command"""
    return COMP_MNEM_BINARY_MAP[comp_mnem]


JUMP_MNEM_BINARY_MAP = {
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}


def jump(jump_mnem: str) -> str:
    """Return the binary code of the 'jump' part of a C-Command"""
    if jump_mnem:
        return JUMP_MNEM_BINARY_MAP[jump_mnem]
    return '000'
