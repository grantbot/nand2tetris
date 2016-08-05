"""Parser module of the Assembler"""

import enum
import io
import os


class CommandType(enum.Enum):
    A = 'A_COMMAND'
    C = 'C_COMMAND'
    L = 'L_COMMAND'


class Parser:
    """Load and interpret an .asm file. See p. 113 for documentation."""
    def __init__(self, file_path: str):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.abs_file_path = os.path.join(dir_path, file_path)

        self.file_obj = open(self.abs_file_path)
        self.current_command = None
        self.current_command_raw = None

    def __enter__(self):
        return self

    def has_more_commands(self) -> bool:
        current_pos = self.file_obj.tell()
        size = os.fstat(self.file_obj.fileno()).st_size
        return current_pos < size

    def advance(self):
        if self.has_more_commands():
            self.current_command_raw = self.file_obj.readline()
            self.current_command = self.current_command_raw.strip('\n ')
            return self.current_command

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

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_obj.close()
