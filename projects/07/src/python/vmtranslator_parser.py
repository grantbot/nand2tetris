"""Parser module for the VM Translator. Mostly cribbed from assembler_parser.py"""

import enum
import os


class CommandType(enum.Enum):
    """Allowed types for VM commands"""
    # Stack arithmetic and manipulation commands, p. 130
    arithmetic = 'C_ARITHMETIC'
    push = 'C_PUSH'
    pop = 'C_POP'

    # Program flow commands, p. 133
    label = 'C_LABEL'
    goto = 'C_GOTO'
    _if = 'C_IF'

    # Function calling commands, p. 133
    function = 'C_FUNCTION'
    call = 'C_CALL'
    _return = 'C_RETURN'


class Parser:
    """Load and read a .vm file.

    Encapsulates access to a .vm file. Reads VM commands, parses them, and
    provides convenient access to the command’s type and arguments. Also
    removes all white space and comments. See p. 144 for API documentation.
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
        current_pos = self.file_obj.tell()
        next_line = self.file_obj.readline()

        # Turns out tell() is useless for anything other than passing to
        # seek()--thus, comparing it with os.stat(file_obj.fileno()).st_size
        # won't work. https://bugs.python.org/issue26016
        # Instead, we must rely on the fact that readline() returns '' at EOF.
        # We should just be doing `for line in f.readlines()` but I'm
        # sticking to the API on p. 113 cuz why not.
        self.file_obj.seek(current_pos)

        # readline() returns '' at EOF
        return next_line != ''

    def advance(self) -> str:
        """Load the next command, skipping if it's a comment or newline."""
        if not self.has_more_commands():
            raise StopIteration('No more commands!')  # Not __next__ but w/e

        self.current_command_raw = self.file_obj.readline()
        self.current_command = self._clean(self.current_command_raw)
        self.current_command_split = self.current_command.split()
        return self.current_command if self.current_command else self.advance()

    def command_type(self) -> CommandType:
        split = self.current_command_split

        if self.is_arithmetic(split):
            return CommandType.arithmetic
        elif self.is_push(split):
            return CommandType.push
        elif self.is_pop(split):
            return CommandType.pop
        elif self.is_label(split):
            return CommandType.label
        elif self.is_goto(split):
            return CommandType.goto
        elif self.is_if(split):
            return CommandType._if
        elif self.is_function(split):
            return CommandType.function
        elif self.is_call(split):
            return CommandType.call
        elif self.is_return(split):
            return CommandType._return
        else:
            raise RuntimeError('Unknown command type: %s' % split)

    def arg1(self) -> str:
        """Returns the first argument of the current command.

        In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is
        returned. Should not be called if the current command is C_RETURN.
        """
        if self.command_type() is CommandType.arithmetic:
            return self.current_command

        if self.command_type() is CommandType._return:
            raise RuntimeError('Cannot call arg1 on CommandType._return')

        return self.current_command_split[1]

    def arg2(self) -> int:
        """Returns the second argument of the current command.

        Should be called only if the current command is C_PUSH, C_POP,
        C_FUNCTION, or C_CALL.
        """
        if self.command_type() not in (
            CommandType.push,
            CommandType.pop,
            CommandType.function,
            CommandType.call,
        ):
            raise RuntimeError('Cannot call arg2 on command type: %s' % self.command_type().value)

        return int(self.current_command_split[2])

    # CommandType checkers
    @staticmethod
    def is_arithmetic(command: [str]) -> bool:
        arith_commands = (
            'add',
            'sub',
            'neg',
            'eq',
            'gt',
            'lt',
            'and',
            'or',
            'not',
        )

        return len(command) == 1 and command[0] in arith_commands

    @staticmethod
    def is_push(command: [str]) -> bool:
        return len(command) == 3 and command[0] == 'push'

    @staticmethod
    def is_pop(command: [str]) -> bool:
        return len(command) == 3 and command[0] == 'pop'

    @staticmethod
    def is_label(command: [str]) -> bool:
        return len(command) == 2 and command[0] == 'label'

    @staticmethod
    def is_goto(command: [str]) -> bool:
        return len(command) == 2 and command[0] == 'goto'

    @staticmethod
    def is_if(command: [str]) -> bool:
        return len(command) == 2 and command[0] == 'if-goto'

    @staticmethod
    def is_function(command: [str]) -> bool:
        return len(command) == 3 and command[0] == 'function'

    @staticmethod
    def is_call(command: [str]) -> bool:
        return len(command) == 3 and command[0] == 'call'

    @staticmethod
    def is_return(command: [str]) -> bool:
        return len(command) == 1 and command[0] == 'return'

    @staticmethod
    def _clean(raw_command: str) -> str:
        """Remove newlines, whitespace, and comments.

        If raw_command is '\n' or consists of only a comment and whitespace
        this will return ''.
        """
        return raw_command.split('//')[0].strip('\n ')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_obj.close()
