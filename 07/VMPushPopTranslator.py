import sys

import VMCommand
from VMArithmeticTranslator import VMArithmeticTranslator
from VMParser import VMParser
from VMWriter import VMWriter




class VMPushPopTranslator:
    VIRTUAL_MEMORY_SEGMENTS = {
        'local': {'base_address_pointer': '1'},
        'argument': {'base_address_pointer': '2'},
        'this': {'base_address_pointer': '3'},
        'that': {'base_address_pointer': '4'}
    }

    POINTER_SEGMENT_BASE_ADDRESS = '3'

    HOST_SEGMENTS = {
        'temp': {'base_address': '5'},
        'static': {'base_address': '16'}
    }

    def translate(self, command):
        #if command.VMCommand.operation() == 'push':
        if command.operation() == 'push':
            return [
                *self.load_desired_value_into_D_instructions_for(segment=command.segment(), index=command.index()),
                *self.place_value_in_D_on_top_of_stack_instructions(),
                *self.increment_stack_pointer_instructions()
            ]
        else:
            return [
                *self.store_top_of_stack_in_D_instructions(),
                *self.store_top_of_stack_first_temp_register_instructions(),
                *self.load_base_address_instructions_for(segment=command.segment()),
                *self.add_index_to_base_address_in_D_instructions(index=command.index()),
                *self.store_target_address_in_second_temp_register_instructions(),
                *self.set_target_address_to_value_instructions()
            ]

    def load_desired_value_into_D_instructions_for(self, segment, index):
        if segment == 'constant':
            return [
                *self.load_value_in_D_instructions(value=index)
            ]
        else:
            return [
                *self.load_base_address_instructions_for(segment=segment),
                *self.add_index_to_base_address_in_D_instructions(index=index),
                *self.load_value_at_memory_address_in_D_instructions()
            ]

    def load_base_address_instructions_for(self, segment):
        if segment in self.VIRTUAL_MEMORY_SEGMENTS:
            pointer_to_segment_base_address = self.VIRTUAL_MEMORY_SEGMENTS[segment]['base_address_pointer']
            return self.load_referenced_value_in_D_instructions(address=pointer_to_segment_base_address)
        elif segment in self.HOST_SEGMENTS:
            host_segment_base_address = self.HOST_SEGMENTS[segment]['base_address']
            return self.load_value_in_D_instructions(value=host_segment_base_address)
        elif segment == 'pointer':
            return self.load_value_in_D_instructions(value=self.POINTER_SEGMENT_BASE_ADDRESS)

    def place_value_in_D_on_top_of_stack_instructions(self):
        return [
            '@SP',
            'A=M',
            'M=D'
        ]

    def increment_stack_pointer_instructions(self):
        return [
            '@SP',
            'M=M+1'
        ]

    def load_referenced_value_in_D_instructions(self, address):
        return [
            '@' + address,
            'D=M'
        ]

    def load_value_in_D_instructions(self, value):
        return [
            '@' + value,
            'D=A'
        ]

    def add_index_to_base_address_in_D_instructions(self, index):
        return [
            '@' + index,
            'D=D+A'
        ]

    def load_value_at_memory_address_in_D_instructions(self):
        return [
            'A=D',
            'D=M'
        ]

    def set_address_to_top_of_stack_instructions(self, address):
        return [
            '@' + address,
            'M=D'
        ]

    def set_target_address_to_value_instructions(self):
        return [
            # load top of stack value
            '@R5',
            # store in D
            'D=M',
            # load segment + index address
            '@R6',
            # set as current address register
            'A=M',
            # set segment[index] to stack top
            'M=D'
        ]

    def store_target_address_in_second_temp_register_instructions(self):
        return [
            # load temp
            '@R6',
            # store segment + index address
            'M=D'
        ]

    def store_top_of_stack_first_temp_register_instructions(self):
        return [
            # load temp register
            '@R5',
            # store top of stack in temp register
            'M=D'
        ]

    def store_top_of_stack_in_D_instructions(self):
        return [
            # load stack pointer
            '@SP',
            # decrement pointer to top of stack
            'AM=M-1',
            # store value in D
            'D=M'
        ]


