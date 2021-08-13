import Code, Parse, symbolTable, sys


class Assembler(object):
    def __init__(self, path):
        self.parser = Parse.Parse(path)
        self.Code = Code.Code()
        self.symbols = symbolTable.SymbolTable()
        self.SymbolAddress = 16
        ind1 = path.find('/')
        ind2 = path.find('.')
        writefile = path[:ind1] + "/" + path[ind1 + 1:ind2]
        self.file = open(writefile + '.hack', 'w')

    def _binary(self, s):
        return bin(int(s))[2:]

    def passA(self):
        curAddress = 0
        while self.parser.hasMoreCommands():
            self.parser.nextStep()
            cmd = self.parser.commandType()
            if cmd in ['A_COMMAND', 'C_COMMAND']:
                curAddress += 1
            elif cmd == 'L_COMMAND':
                self.symbols.addEntry(self.parser.symbol(), curAddress)
            else:
                raise ValueError("Unexpected command type encountered")

    def passB(self):
        self.parser.i = -1
        while self.parser.hasMoreCommands():
            self.parser.nextStep()
            cmd = self.parser.commandType()
            if cmd == 'A_COMMAND':
                symbol = self.parser.symbol()
                if (not symbol.isdigit()) and (not self.symbols.contains(symbol)):
                    self.symbols.addEntry(symbol, self.SymbolAddress)
                    self.SymbolAddress += 1

    def createOut(self):
        self.parser.i = -1
        while self.parser.hasMoreCommands():
            self.parser.nextStep()
            cmd = self.parser.commandType()
            if cmd == 'A_COMMAND':
                symbol = self.parser.symbol()
                if symbol.isdigit():
                    binSymbol = self._binary(symbol)
                else:
                    symbAdd = self.symbols.getAddress(symbol)
                    binSymbol = self._binary(symbAdd)
                aCmnd = '0' * (16 - len(binSymbol)) + binSymbol
                self.file.write(aCmnd + '\n')
            elif cmd == 'C_COMMAND':
                dstMnem = self.parser.dest()
                dest = self.Code.dest(dstMnem)
                cmpMnem = self.parser.comp()
                comp = self.Code.comp(cmpMnem)
                jmpMnem = self.parser.jump()
                jump = self.Code.jump(jmpMnem)
                cCmnd = '111' + comp + dest + jump
                self.file.write(cCmnd + '\n')
            else:
                pass
        self.file.close()


if __name__ == '__main__':
    assemb_symb = Assembler(sys.argv[1])
    assemb_symb.passA()
    assemb_symb.passB()
    assemb_symb.createOut()
