class VMWriter:
    def __init__(self, input_file):
        self.output_file = open(self._output_file_name_from(input_file), 'w')

    def write(self, command):
        self.output_file.write(command)

    def close_file(self):
        self.output_file.close()

    @staticmethod
    def _output_file_name_from(file):
        return file.split('.')[0] + '.asm'
