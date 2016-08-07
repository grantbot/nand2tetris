"""Entry point for the Assembler"""

import typing

import assembler_parser
import assembler_code
import assembler_symbol


def asm_to_hack(filename: str) -> typing.Iterable(str):
    """Convert an .asm file to Hack binary"""
    with assembler_parser.Parser(filename) as asm:
        while asm.has_more_commands():
            command_type = _next_command(asm)

            if command_type is assembler_parser.CommandType.A:
                yield format(int(asm.symbol()), '016b')

            elif command_type is assembler_parser.CommandType.C:
                dest = assembler_code.dest(asm.dest())
                comp, a_bit = assembler_code.comp(asm.comp())
                jump = assembler_code.jump(asm.jump())

                result = '111' + a_bit + comp + dest + jump
                assert len(result) == 16
                yield result


def extract_labels(
        asm_obj: assembler_parser.Parser,
        sym_table: assembler_symbol.SymbolTable) -> assembler_symbol.SymbolTable:

    instr_counter = 1
    while asm_obj.has_more_commands():
        command_type = _next_command(asm_obj)
        if command_type is assembler_parser.CommandType.L:
            sym_table.add_entry(asm_obj.symbol(), instr_counter)
            continue
        instr_counter += 1

    return sym_table


def _next_command(asm_obj: assembler_parser.Parser) -> assembler_parser.CommandType:
    asm_obj.advance()
    return asm_obj.command_type()
