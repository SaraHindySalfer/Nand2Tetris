import sys
import re
from VMCommand import VMCommand


class VMParser:
    def __init__(self, file):
        self.input_file = open(file, 'r')
        self.has_more_commands = True
        self.current_command = None
        self.next_command = None

    def has_valid_current_command(self):
        return not self.current_command.is_whitespace() and not self.current_command.is_comment()

    def advance(self):
        self._update_current_command()
        self._update_next_command()
        self._update_has_more_commands()

    def _update_has_more_commands(self):
        if self.next_command.is_empty():
            self.has_more_commands = False

    def _update_next_command(self):
        text = self.input_file.readline()
        self.next_command = VMCommand(text)

    def _update_current_command(self):
        if self.current_command == None:
            text = self.input_file.readline()
            self.current_command = VMCommand(text)
        else:
            self.current_command = self.next_command
