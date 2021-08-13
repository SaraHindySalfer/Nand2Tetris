class VMArithmeticTranslator:
    OPERATION_INSTRUCTIONS = {
        'add': 'M=M+D',
        'sub': 'M=M-D',
        'neg': 'M=-M',
        'or': 'M=M|D',
        'not': 'M=!M',
        'and': 'M=M&D'
    }

    COMP_COMMANDS = {
        'eq': {'jump_directive': 'JNE'},
        'lt': {'jump_directive': 'JGE'},
        'gt': {'jump_directive': 'JLE'}
    }

    def __init__(self):
        self.comp_counters = {
            'eq': {'count': 0},
            'lt': {'count': 0},
            'gt': {'count': 0}
        }

    def translate(self, command):
        if command.text in self.COMP_COMMANDS:
            return self.comp_translation(command.text)

    def arithmetic_translation(self, command_text):
        if command_text in ['add', 'sub', 'and', 'or']:
            return [
                *self.pop_top_number_off_stack_instructions(),
                'D=M',
                *self.pop_top_number_off_stack_instructions(),
                self.OPERATION_INSTRUCTIONS[command_text],
                *self.increment_stack_pointer_instructions(),
            ]
        else:
            return [
                *self.pop_top_number_off_stack_instructions(),
                self.OPERATION_INSTRUCTIONS[command_text],
                *self.increment_stack_pointer_instructions(),
            ]

    def comp_translation(self, command_text):
        counter = self.comp_counters[command_text]
        counter['count'] += 1
        label_identifier = '{}{}'.format(command_text.upper(), counter['count'])
        jump_directive = self.COMP_COMMANDS[command_text]['jump_directive']
        return [
            *self.pop_top_number_off_stack_instructions(),
            'D=M',
            *self.pop_top_number_off_stack_instructions(),
            'D=M-D',
            '@NOT_{}'.format(label_identifier),
            'D;{}'.format(jump_directive),
            '@SP',
            'A=M',
            'M=-1',
            '@INC_STACK_POINTER_{}'.format(label_identifier),
            '0;JMP',
            '(NOT_{})'.format(label_identifier),
            '@SP',
            'A=M',
            'M=0',
            '(INC_STACK_POINTER_{})'.format(label_identifier),
            *self.increment_stack_pointer_instructions(),
        ]

    def pop_top_number_off_stack_instructions(self):
        return [
            '@SP',
            'AM=M-1'
        ]

    def increment_stack_pointer_instructions(self):
        return [
            '@SP',
            'M=M+1'
        ]
