"""Tests for the Parser module of the Assembler"""

import io

import pytest

import assembler_parser as parser


# TODO pytest.mark.parametrize is dope, refactor some of these tests
class TestAssemblerParser:

    def test_parser_init(self):
        with parser.Parser('testfiles/test.asm') as p:
            assert isinstance(p.file_obj, io.IOBase)

    def test_has_more_commands(self):
        with parser.Parser('testfiles/test.asm') as p:
            for _ in range(10):
                assert p.has_more_commands() is True
                p.file_obj.readline()

            assert p.has_more_commands() is False

    def test_advance(self):
        with parser.Parser('testfiles/test.asm') as p:
            assert p.advance() == '(START)'
            assert p.current_command_raw == '(START)\n'

            assert p.advance() == '@0'
            assert p.current_command_raw == '      @0\n'

            assert p.advance() == '@var'
            assert p.current_command_raw == '    @var  // comment\n'

    def test_command_type(self):
        with parser.Parser('testfiles/test.asm') as p:
            assert p.advance() == '(START)'
            assert p.command_type() == parser.CommandType.L

            assert p.advance() == '@0'
            assert p.command_type() == parser.CommandType.Anum

            assert p.advance() == '@var'
            assert p.command_type() == parser.CommandType.Avar

            assert p.advance() == 'D=A'
            assert p.command_type() == parser.CommandType.C

            assert p.advance() == 'AM=D+A'
            assert p.command_type() == parser.CommandType.C

            assert p.advance() == 'D;JGT'
            assert p.command_type() == parser.CommandType.C

    def test_symbol(self):
        with parser.Parser('testfiles/test.asm') as p:
            assert p.advance() == '(START)'
            assert p.symbol() == 'START'

            assert p.advance() == '@0'
            assert p.symbol() == '0'

            assert p.advance() == '@var'
            assert p.symbol() == 'var'

            assert p.advance() == 'D=A'
            assert p.symbol() is None

            assert p.advance() == 'AM=D+A'
            assert p.symbol() is None

            assert p.advance() == 'D;JGT'
            assert p.symbol() is None

    def test_dest(self):
        with parser.Parser('testfiles/test.asm') as p:
            assert p.advance() == '(START)'
            assert p.dest() is None

            assert p.advance() == '@0'
            assert p.dest() is None

            assert p.advance() == '@var'
            assert p.dest() is None

            assert p.advance() == 'D=A'
            assert p.dest() == 'D'

            assert p.advance() == 'AM=D+A'
            assert p.dest() == 'AM'

            assert p.advance() == 'D;JGT'
            assert p.dest() is None

    def test_comp(self):
        with parser.Parser('testfiles/test.asm') as p:
            assert p.advance() == '(START)'
            assert p.comp() is None

            assert p.advance() == '@0'
            assert p.comp() is None

            assert p.advance() == '@var'
            assert p.comp() is None

            assert p.advance() == 'D=A'
            assert p.comp() == 'A'

            assert p.advance() == 'AM=D+A'
            assert p.comp() == 'D+A'

            assert p.advance() == 'D;JGT'
            assert p.comp() == 'D'

            assert p.advance() == '(END)'
            assert p.comp() is None

            assert p.advance() == '0;JMP'
            assert p.comp() == '0'

    def test_jump(self):
        with parser.Parser('testfiles/test.asm') as p:
            assert p.advance() == '(START)'
            assert p.jump() is None

            assert p.advance() == '@0'
            assert p.jump() is None

            assert p.advance() == '@var'
            assert p.jump() is None

            assert p.advance() == 'D=A'
            assert p.jump() is None

            assert p.advance() == 'AM=D+A'
            assert p.jump() is None

            assert p.advance() == 'D;JGT'
            assert p.jump() == 'JGT'

            assert p.advance() == '(END)'
            assert p.jump() is None

            assert p.advance() == '0;JMP'
            assert p.jump() == 'JMP'

    @pytest.mark.parametrize('input_str, expected', [
        ('@var'               , '@var'),
        ('     @var  // comm' , '@var'),
        ('     D;JGT'         , 'D;JGT'),
        ('     D;JGT  // comm', 'D;JGT'),
        ('     AM=D+A'        , 'AM=D+A'),
        ('     D=A  // comm'  , 'D=A'),
        ('// comment'         , ''),
        ('   // comment'      , ''),
        ('\n'                 , ''),
    ])
    def test_clean(self, input_str, expected):
        clean = parser.Parser._clean
        assert clean(input_str) == expected

    @pytest.mark.parametrize('input_str, expected', [
        ('@123', True),
        ('@0123', True),
        ('@1', True),
        ('@i', False),
        ('@var', False),
    ])
    def test_is_a_num_command(self, input_str, expected):
        is_a_num = parser.Parser._is_a_num_command
        assert is_a_num(input_str) is expected

    @pytest.mark.parametrize('input_str, expected', [
        ('@123', False),
        ('@0123', False),
        ('@1', False),
        ('@9var', False),
        ('@i', True),
        ('@var', True),
        ('@var:$', True),
        ('@var1', True),
        ('@var1.0', True),
        ('@some_var', True),
    ])
    def test_is_a_var_command(self, input_str, expected):
        is_a_var = parser.Parser._is_a_var_command
        assert is_a_var(input_str) is expected
