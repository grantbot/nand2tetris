"""Tests for the Parser module of the Assembler"""

import io

import pytest

import assembler_parser


class TestAssemblerParser():

    def test_parser_init(self):
        with assembler_parser.Parser('test.asm') as f:
            assert isinstance(f.file_obj, io.IOBase)

    def test_has_more_commands(self):
        with assembler_parser.Parser('test.asm') as f:
            for _ in range(8):
                assert f.has_more_commands() is True
                f.file_obj.readline()

            assert f.has_more_commands() is False

    def test_advance(self):
        with assembler_parser.Parser('test.asm') as f:
            # Read first two lines
            assert f.advance() == '(START)'
            assert f.current_command_raw == '(START)\n'

            assert f.advance() == '@0'
            assert f.current_command_raw == '      @0\n'


    def test_command_type(self):
        with assembler_parser.Parser('test.asm') as f:
            assert f.advance() == '(START)'
            assert f.command_type() == assembler_parser.CommandType.L

            assert f.advance() == '@0'
            assert f.command_type() == assembler_parser.CommandType.A

            assert f.advance() == '@var'
            assert f.command_type() == assembler_parser.CommandType.A

            assert f.advance() == 'D=A'
            assert f.command_type() == assembler_parser.CommandType.C

            assert f.advance() == 'AM=D+A'
            assert f.command_type() == assembler_parser.CommandType.C

            assert f.advance() == 'D;JGT'
            assert f.command_type() == assembler_parser.CommandType.C

    def test_symbol(self):
        with assembler_parser.Parser('test.asm') as f:
            assert f.advance() == '(START)'
            assert f.symbol() == 'START'

            assert f.advance() == '@0'
            assert f.symbol() == '0'

            assert f.advance() == '@var'
            assert f.symbol() == 'var'

            assert f.advance() == 'D=A'
            assert f.symbol() == None

            assert f.advance() == 'AM=D+A'
            assert f.symbol() == None

            assert f.advance() == 'D;JGT'
            assert f.symbol() == None

    def test_dest(self):
        with assembler_parser.Parser('test.asm') as f:
            assert f.advance() == '(START)'
            assert f.dest() == None

            assert f.advance() == '@0'
            assert f.dest() == None

            assert f.advance() == '@var'
            assert f.dest() == None

            assert f.advance() == 'D=A'
            assert f.dest() == 'D'

            assert f.advance() == 'AM=D+A'
            assert f.dest() == 'AM'

            assert f.advance() == 'D;JGT'
            assert f.dest() == None

    def test_comp(self):
        with assembler_parser.Parser('test.asm') as f:
            assert f.advance() == '(START)'
            assert f.comp() == None

            assert f.advance() == '@0'
            assert f.comp() == None

            assert f.advance() == '@var'
            assert f.comp() == None

            assert f.advance() == 'D=A'
            assert f.comp() == None

            assert f.advance() == 'AM=D+A'
            assert f.comp() == None

            assert f.advance() == 'D;JGT'
            assert f.comp() == 'D'

            assert f.advance() == '0;JMP'
            assert f.comp() == '0'

    def test_jump(self):
        with assembler_parser.Parser('test.asm') as f:
            assert f.advance() == '(START)'
            assert f.jump() == None

            assert f.advance() == '@0'
            assert f.jump() == None

            assert f.advance() == '@var'
            assert f.jump() == None

            assert f.advance() == 'D=A'
            assert f.jump() == None

            assert f.advance() == 'AM=D+A'
            assert f.jump() == None

            assert f.advance() == 'D;JGT'
            assert f.jump() == 'JGT'

            assert f.advance() == '0;JMP'
            assert f.jump() == 'JMP'
