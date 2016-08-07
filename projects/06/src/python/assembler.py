"""Entry point for the Assembler"""

import typing

import assembler_parser
import assembler_code


def asm_to_hack(filename: str) -> typing.Iterable(str):
    """Convert an .asm file to Hack binary"""
    with assembler_parser.Parser(filename) as asm:
        while asm.has_more_commands():
            asm.advance()

            command_type = asm.command_type()

            if command_type is assembler_parser.CommandType.A:
                yield format(int(asm.symbol()), '016b')

            elif command_type is assembler_parser.CommandType.C:
                dest = assembler_code.dest(asm.dest())
                comp, a_bit = assembler_code.comp(asm.comp())
                jump = assembler_code.jump(asm.jump())

                result = '111' + a_bit + comp + dest + jump
                assert len(result) == 16
                yield result
