"""Entry point for the Assembler"""

import typing

import assembler_parser as parser
import assembler_code as code
import assembler_symbol as symbol

BINARY_FMT = '016b'


def asm_to_hack(filename: str) -> typing.Iterable(str):
    """Convert an .asm file to Hack binary"""
    with parser.Parser(filename) as asm:
        # First Pass: init symbol table and extract label pseudocommands
        sym_table = extract_labels(asm)

        asm.file_obj.seek(0)

        # Second Pass: Generate binary .hack commands
        while asm.has_more_commands():
            command_type = _next_command(asm)

            # @ commands
            sym = asm.symbol()
            if command_type is parser.CommandType.Anum:
                yield format(int(sym), BINARY_FMT)
            elif command_type is parser.CommandType.Avar:
                sym_table.contains(sym) or sym_table.add_entry(sym)
                yield format(sym_table.get_address(sym), BINARY_FMT)

            elif command_type is parser.CommandType.C:
                dest = code.dest(asm.dest())
                comp, a_bit = code.comp(asm.comp())
                jump = code.jump(asm.jump())

                result = '111' + a_bit + comp + dest + jump
                assert len(result) == 16
                yield result


def extract_labels(asm_obj: parser.Parser) -> symbol.SymbolTable:
    """Save label pseudocommands into a given symbol table"""
    instr_counter = 1
    sym_table = symbol.SymbolTable()

    while asm_obj.has_more_commands():
        command_type = _next_command(asm_obj)

        if command_type is parser.CommandType.L:
            sym_table.add_entry(asm_obj.symbol(), instr_counter)
            continue

        instr_counter += 1

    return sym_table


def _next_command(asm_obj: parser.Parser) -> parser.CommandType:
    asm_obj.advance()
    return asm_obj.command_type()
