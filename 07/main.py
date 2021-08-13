import sys

from VMArithmeticTranslator import VMArithmeticTranslator
from VMParser import VMParser
from VMPushPopTranslator import VMPushPopTranslator
from VMWriter import VMWriter

if __name__ == "__main__":
    # and len(sys.argv) == 2:
    # vm_code_file = sys.argv[1]
    vm_code_file = 'StackArithmetic/SimpleAdd/SimpleAdd.vm'
    parser = VMParser(vm_code_file)
    writer = VMWriter(vm_code_file)
    arithmetic_translator = VMArithmeticTranslator()
    push_pop_translator = VMPushPopTranslator()

    while parser.has_more_commands:
        parser.advance()
        translation = []

        if parser.has_valid_current_command():
            if parser.current_command.is_push_pop_command():
                translation = push_pop_translator.translate(parser.current_command)
            else:
                translation = arithmetic_translator.translate(parser.current_command)

            for line in translation:
                writer.write(line + '\n')

    writer.close_file()
