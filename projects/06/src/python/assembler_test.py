import itertools
from functools import partial

import pytest

import assembler
import assembler_parser as parser
import assembler_symbol as symbol


class TestAssembler:

    def test_extract_labels(self):
        with parser.Parser('testfiles/test.asm') as p:
            sym_table = assembler.extract_labels(p)

        assert sym_table.get_address('START') == 0
        assert sym_table.get_address('END') == 5
        assert len(sym_table._table.keys()) == len(symbol.DEFAULT_LABELS.keys()) + 2

    @pytest.mark.parametrize('asm_input_path, expected_binary_output_path', [
        ('testfiles/Add.asm', 'testfiles/Add.hack'),
    ])
    def test_assembler(self, asm_input_path, expected_binary_output_path):
        # Gen test output
        hack_commands = assembler.asm_to_hack(asm_input_path)

        # Load expected .hack output
        with parser.Parser(expected_binary_output_path) as p:
            expected = p.file_obj

            # zip_longest, combined with the below assertions against None-ness,
            # ensure that we're generating the right number of commands.
            comparisons = itertools.zip_longest(
                hack_commands,
                iter(partial(self._stream, expected), '')
            )

            for comp in comparisons:
                test_output = comp[0]
                expected = comp[1]
                assert test_output is not None and expected is not None
                assert test_output == expected

    @staticmethod
    def _stream(file_obj):
        return file_obj.readline().strip()
