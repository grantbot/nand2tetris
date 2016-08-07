"""Tests for the Symobl module of the Assembler"""

import pytest

import assembler_symbol as symbol


class TestSymbolTable:

    @pytest.fixture
    def sym_table(self):
        return symbol.SymbolTable()

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
        sym_table.add_entry('foo', 16)
        assert sym_table._table['foo'] == 16

    def test_add_entry_overwrite_default(self, sym_table):
        with pytest.raises(ValueError):
            sym_table.add_entry('R0', 999)
