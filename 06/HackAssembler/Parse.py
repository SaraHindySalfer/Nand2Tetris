class Parse:
    def __init__(self, path):
        f = open(path, 'r')
        rawLines = f.readlines()
        self.cleanLines = []
        for line in rawLines:
            if (line[:2] == '//') or (line == '\n'):
                continue
            else:
                pass
            if '//' in line:
                line = line[:line.find('//')]
            line = line.replace(' ', '')
            l = []
            for ch in line:
                if ch not in [" ", "\n"]:
                    l.append(ch)
            self.cleanLines.append(''.join(l))
        self.i = -1
        self.command = None
        self.totalCommands = len(self.cleanLines)

    def hasMoreCommands(self):
        return self.i < self.totalCommands - 1

    def nextStep(self):
        if self.hasMoreCommands():
            self.i += 1
            self.command = self.cleanLines[self.i]

    def commandType(self):
        if self.command[0] == '@':
            return 'A_COMMAND'
        elif self.command[0] == '(':
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    def symbol(self):
        if self.commandType() == 'A_COMMAND':
            return self.command[1:]
        elif self.commandType() == 'L_COMMAND':
            return self.command[1:-1]
        else:
            raise ValueError("Command type should be A or L")

    def dest(self):
        if self.commandType() == 'C_COMMAND':
            ind = self.command.find('=')
            if ind != -1:
                return self.command[:ind]
            else:
                return 'null'
        else:
            raise ValueError("Command type should be A or L")

    def comp(self):
        if self.commandType() == 'C_COMMAND':
            ind1 = self.command.find('=')
            ind2 = self.command.find(';')
            if (ind1 != -1) and (ind2 != -1):
                return self.command[ind1 + 1:ind2]
            elif (ind1 != -1) and (ind2 == -1):
                return self.command[ind1 + 1:]
            elif (ind1 == -1) and (ind2 != -1):
                return self.command[:ind2]
            elif (ind1 == -1) and (ind2 == -1):
                return self.command
            else:
                return 'null'
        else:
            raise ValueError("Command type should be A or L")

    def jump(self):
        if self.commandType() == 'C_COMMAND':
            ind = self.command.find(';')
            if ind != -1:
                return self.command[ind + 1:]
            else:
                return 'null'
        else:
            raise ValueError("Command type should be A or L")
