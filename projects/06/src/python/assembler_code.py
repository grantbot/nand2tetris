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
    # Where 'X' can be either 'A' or 'M'. Does not affect comp mnemonic parsing.
    '0': '101010',
    '1': '111111',
    '-1': '111010',
    'D': '001100',
    'X': '110000',
    '!D': '001101',
    '!X': '110001',
    '-D': '001111',
    '-X': '110001',
    'D+1': '011111',
    'X+1': '110111',
    'D-1': '001110',
    'X-1': '110010',
    'D+X': '000010',
    'D-X': '010011',
    'X-D': '000111',
    'D&X': '000000',
    'D|X': '010101',
}


def comp(comp_mnem: str) -> str:
    """Return the binary code of the 'comp' part of a C-Command

    Also returns the appropriate value for the a-bit of a C-Command, depening
    on whether A or M is used in the calculation.
    """
    a_bit = '1' if 'M' in comp_mnem else '0'
    normalized = comp_mnem.replace('A', 'X').replace('M', 'X')
    return COMP_MNEM_BINARY_MAP[normalized], a_bit


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
