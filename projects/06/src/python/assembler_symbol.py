"""Symobl module of the Assembler"""

# Convenience pointers to specific memory addresses
DEFAULT_LABELS = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'SCREEN': 16384,
    'KBD': 24576,
}


class SymbolTable:
    """Store/access variable (RAM addresses) and label (ROM addresses) pointers

    Pre-defined symbols are specified on p. 69.
    """
    def __init__(self):
        self._table = DEFAULT_LABELS.copy()
        self._curr_ram_addr = 15

    def add_entry(self, symbol: str, address: int=None) -> None:
        if symbol in DEFAULT_LABELS:
            raise ValueError('No overwriting default labels!')

        # If `address` is given then `symbol` is a label (ROM address),
        # otherwise it's a new variable (RAM address).
        address = address if address is not None else self._incr_ram_addr()
        self._table[symbol] = int(address)

    def contains(self, symbol: str) -> bool:
        return symbol in self._table

    def get_address(self, symbol: str) -> int:
        return self._table[symbol]

    def _incr_ram_addr(self):
        self._curr_ram_addr += 1
        return self._curr_ram_addr
