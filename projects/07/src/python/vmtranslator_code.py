"""Code module for the VM Translator"""

import vmtranslator_parser as parser


class Code:
    """Translate VM commands to Hack Machine Language"""

    def set_filename(self, filename: str):
        self.filename = filename

    def write_arithmetic(self, command: str):
        pass

    def write_pushpop(self, command: parser.CommandType, segment: str, index: int):
        pass
