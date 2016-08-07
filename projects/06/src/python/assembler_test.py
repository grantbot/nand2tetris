import itertools
from functools import partial

import assembler
import assembler_parser
import assembler_symbol


class TestAssembler:

    def test_extract_labels(self):
        sym_table = assembler_symbol.SymbolTable()

        with assembler_parser.Parser('test.asm') as p:
            sym_table = assembler.extract_labels(p, sym_table)

        assert sym_table.get_address('START') == 1
        assert sym_table.get_address('END') == 6
        assert len(sym_table._table.keys()) == len(assembler_symbol.DEFAULT_LABELS.keys()) + 2

    def test_add_sans_symbols(self):
        # Gen test output
        hack_commands = assembler.asm_to_hack('Add.asm')

        # Load expected .hack output
        with assembler_parser.Parser('Add.hack') as p:
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
