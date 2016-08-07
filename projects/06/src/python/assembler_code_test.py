"""Tests for the Code module of the Assembler"""

import pytest

import assembler_code


class TestAssemblerCode:

    @pytest.mark.parametrize('test_input, expected', [
        ('D;JGT', '000'),
        ('M=M+D', '001'),
        ('D=M+D', '010'),
        ('MD=M+D', '011'),
        ('A=M+D', '100'),
        ('AM=M+D', '101'),
        ('AD=M+D', '110'),
        ('AMD=M+D', '111'),
    ])
    def test_dest(self, test_input, expected):
        assert assembler_code.dest(test_input) == expected

    @pytest.mark.parametrize('comp_input, expected', [
        ('0', '101010'),
        ('1', '111111'),
        ('-1', '111010'),
        ('D', '001100'),
        ('A', '110000'),
        ('!D', '001101'),
        ('!A', '110001'),
        ('-D', '001111'),
        ('-A', '110001'),
        ('D+1', '011111'),
        ('A+1', '110111'),
        ('D-1', '001110'),
        ('A-1', '110010'),
        ('D+A', '000010'),
        ('D-A', '010011'),
        ('A-D', '000111'),
        ('D&A', '000000'),
        ('D|A', '010101'),
    ])
    def test_comp(self, comp_input, expected):
        assert assembler_code.comp('D=' + comp_input) == expected
        assert assembler_code.comp('AMD=' + comp_input) == expected
        assert assembler_code.comp(comp_input + ';JGT') == expected
        assert assembler_code.comp(comp_input + ';JMP') == expected

    @pytest.mark.parametrize('jump_input, expected', [
        ('JGT', '001'),
        ('JEQ', '010'),
        ('JGE', '011'),
        ('JLT', '100'),
        ('JNE', '101'),
        ('JLE', '110'),
        ('JMP', '111'),
    ])
    def jump_comp(self, jump_input, expected):
        assert assembler_code.jump('D;' + jump_input) == expected
        assert assembler_code.jump('AMD;' + jump_input) == expected
        assert assembler_code.jump('D=M') == '000'
