"""Parser module of the Assembler"""

import enum
import io
import os


class CommandType(enum.Enum):
    A = 'A_COMMAND'
    C = 'C_COMMAND'
    L = 'L_COMMAND'


class Parser:
    """Load and read an .asm file.

    Encapsulates access to the input code. Reads an assembly language command,
    parses it, and provides convenient access to the command’s components
    (fields and symbols). In addition, removes all white space and comments.
    See p. 113 for API documentation.

    TODO
    - has_more_commands thinks all lines are commands, even if they're a comment
    or just a \n.


    """
    def __init__(self, file_path: str):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.abs_file_path = os.path.join(dir_path, file_path)

        self.file_obj = open(self.abs_file_path)
        self.current_command = None
        self.current_command_raw = None

    def __enter__(self):
        return self

    def has_more_commands(self) -> bool:
        """Check current position relative to file size."""
        current_pos = self.file_obj.tell()
        size = os.fstat(self.file_obj.fileno()).st_size
        return current_pos < size

    def advance(self) -> str:
        """Load the next command, skipping if it's a comment or newline."""
        if not self.has_more_commands():
            raise StopIteration('No more commands!')  # Not __next__ but w/e

        self.current_command_raw = self.file_obj.readline()
        self.current_command = self._clean(self.current_command_raw)
        return self.current_command if self.current_command else self.advance()

    def command_type(self) -> CommandType:
        command = self.current_command
        # TODO Use regexes?
        if '@' in command:
            return CommandType.A
        elif '=' in command or ';' in command:
            return CommandType.C
        elif '(' in command and ')' in command:
            return CommandType.L

    def symbol(self) -> str:
        if self.command_type() in (CommandType.A, CommandType.L):
            return self.current_command.strip('@()')

    def dest(self) -> str:
        if self.command_type() == CommandType.C:
            if '=' in self.current_command:
                return self.current_command.split('=')[0]

    def comp(self) -> str:
        if self.command_type() == CommandType.C:
            if ';' in self.current_command:
                return self.current_command.split(';')[0]

    def jump(self) -> str:
        if self.command_type() == CommandType.C:
            if ';' in self.current_command:
                return self.current_command.split(';')[1]

    @staticmethod
    def _clean(raw_command: str) -> str:
        """Remove newlines, whitespace, and comments.

        If raw_command is '\n' or consists of only a comment and whitespace
        this will return ''.
        """
        return raw_command.split('//')[0].strip('\n ')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_obj.close()
