"""Tests for the Code module of the VM Translator"""

import pytest

import vmtranslator_code as code
import vmtranslator_parser as parser


class TestVMTranslatorCode:

    @pytest.mark.parametrize(
        'command_type, segment, index, expected',
        [
            (parser.CommandType.push, 'constant', 1, [
                '@1',
                'D=A',  # Load desired constant into D-reg
                '@SP',  # Load 0 into A-reg
                'A=M',  # Get address at Memory[0]
                'M=D',  # Push constant to stack
                '@SP'
                'M=M+1'
            ]),
        ]
    )
    def test_push_constant(self):
        translator = code.Code()
        translator.write_pushpop()
