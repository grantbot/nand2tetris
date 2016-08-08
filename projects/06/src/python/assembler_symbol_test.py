"""Tests for the Symobl module of the Assembler"""

import pytest

import assembler_symbol as symbol


@pytest.fixture
def sym_table():
    return symbol.SymbolTable()


class TestSymbolTable:

    @pytest.mark.parametrize('input_symbol, expctd_addr', zip(
        symbol.DEFAULT_LABELS.keys(),
        symbol.DEFAULT_LABELS.values(),
    ))
    def test_init_defaults(self, sym_table, input_symbol, expctd_addr):
        assert sym_table._table[input_symbol] == expctd_addr

    @pytest.mark.parametrize('input_symbol, expctd_addr', zip(
        symbol.DEFAULT_LABELS.keys(),
        symbol.DEFAULT_LABELS.values(),
    ))
    def test_get_address(self, sym_table, input_symbol, expctd_addr):
        assert sym_table.get_address(input_symbol) == expctd_addr

    def test_get_invalid_address(self, sym_table):
        with pytest.raises(KeyError):
            sym_table.get_address('bad_address')

    @pytest.mark.parametrize('input_symbol', symbol.DEFAULT_LABELS.keys())
    def test_contains(self, sym_table, input_symbol):
        assert sym_table.contains(input_symbol) is True

    def test_add_entry(self, sym_table):
        sym_table.add_entry('label', 1)
        assert sym_table._table['label'] == 1

        sym_table.add_entry('other_label', '2')
        assert sym_table._table['other_label'] == 2

        sym_table.add_entry('variable')
        sym_table.add_entry('other_variable')
        assert sym_table._table['variable'] == 16
        assert sym_table._table['other_variable'] == 17

    def test_add_entry_overwrite_default(self, sym_table):
        with pytest.raises(ValueError):
            sym_table.add_entry('R0', 999)
