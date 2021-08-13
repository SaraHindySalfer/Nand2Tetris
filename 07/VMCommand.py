import sys
import re


class VMCommand:
    COMMENT_SYMBOL = '//'
    NEWLINE_SYMBOL = '\n'
    EMPTY_SYMBOL = ' '

    def __init__(self, text):
        self.raw_text = text
        self.text = text.strip()
        self.parts = text.strip().split(' ')

    def is_push_pop_command(self):
        return self.operation() == 'push' or self.operation() == 'pop'

    def is_comment(self):
        return self.raw_text[0:2] == self.COMMENT_SYMBOL

    def is_empty(self):
        return self.raw_text == self.EMPTY_SYMBOL


    def is_whitespace(self):
        return self.raw_text == self.NEWLINE_SYMBOL

    def segment(self):
        if len(self.parts) != 3:
            return
        return self.parts[1]

    def index(self):
        if len(self.parts) != 3:
            return
        return self.parts[2]

    def operation(self):
        return self.parts[0]
