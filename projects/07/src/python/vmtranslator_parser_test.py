"""Tests for the Parser module of the VM Translator"""

import io

import pytest

import vmtranslator_parser as parser

SIMPLE_ADD_PATH = '../../StackArithmetic/SimpleAdd/SimpleAdd.vm'


class TestVMTranslatorParser:

    def test_parser_init(self):
        with parser.Parser(SIMPLE_ADD_PATH) as p:
            assert isinstance(p.file_obj, io.IOBase)

    def test_simple_add_has_more_commands(self):
        with parser.Parser(SIMPLE_ADD_PATH) as p:
            assert p.has_more_commands() is True
            assert p.advance() == 'push constant 7'
            assert p.command_type() is parser.CommandType.push
            assert p.arg1() == 'constant'
            assert p.arg2() == 7

            assert p.has_more_commands() is True
            assert p.advance() == 'push constant 8'
            assert p.command_type() is parser.CommandType.push
            assert p.arg1() == 'constant'
            assert p.arg2() == 8

            assert p.has_more_commands() is True
            assert p.advance() == 'add'
            assert p.command_type() is parser.CommandType.arithmetic
            assert p.arg1() == 'add'

            assert p.has_more_commands() is False
