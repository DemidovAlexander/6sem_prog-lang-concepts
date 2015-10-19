__author__ = 'Alexander Demidov'


class Assembler:
    def __init__(self):
        self.bytecode = []
        self.labels = {}
        self.variables = {}
        self.code = []

        self.read_file()

    @staticmethod
    def get_hex(*nums):
        if len(nums) == 1:
            return format(int(nums[0]), '#010x')
        hex_str = "0x"
        for num in nums:
            hex_str += (format(int(num), '02x'))
        return hex_str

    def run(self):
        for counter, line in enumerate(self.code):
            if line.startswith("LET", 0, len(line)):
                params = line.split(' ')[1:]
                self.variables[params[0]] = counter + 7
                self.bytecode.append(self.get_hex(params[1]))

            if line.find(":", 0, len(line)) > 0:
                label_name = line.strip(':')
                self.labels[label_name] = counter + 7 - len(self.labels)

        self.bytecode = [self.get_hex(len(self.variables) + 7)] + [self.get_hex(0)] * 6 + self.bytecode
        self.compile()
        self.bytecode[2] = self.get_hex(len(self.bytecode))
        self.write_file()

    def compile(self):
        for counter, line in enumerate(self.code):
            params = line.split(' ')[1:]
            if line.startswith("IN"):
                self.bytecode.append(self.get_hex(6, self.variables[params[0]], 0, 0))
            if line.startswith("OUT"):

                self.bytecode.append(self.get_hex(5, self.variables[params[0]], 0, 0))
            if line.startswith("ADD"):
                self.bytecode.append(self.get_hex(3, self.variables[params[0]], self.variables[params[1]], 0))
            if line.startswith("SUB"):
                self.bytecode.append(self.get_hex(1, self.variables[params[0]], self.variables[params[1]], 0))
            if line.startswith("MOV"):
                self.bytecode.append(self.get_hex(2, self.variables[params[0]], self.variables[params[1]], 0))

            if line.startswith("CMP"):
                self.bytecode.append(self.get_hex(4, self.variables[params[0]], self.variables[params[1]], 0))

            if line.startswith("JNQ"):
                self.bytecode.append(self.get_hex(7, self.labels[params[0]], 0, 0))
            if line.startswith("JL"):
                self.bytecode.append(self.get_hex(8, self.labels[params[0]], 0, 0))
            if line.startswith("JQ"):
                self.bytecode.append(self.get_hex(9, self.labels[params[0]], 0, 0))
            if line.startswith("JG"):
                self.bytecode.append(self.get_hex(10, self.labels[params[0]], 0, 0))
            if line.startswith("JMP"):
                self.bytecode.append(self.get_hex(11, self.labels[params[0]], 0, 0))

            if line.startswith("CALL"):
                self.bytecode.append(self.get_hex(12, self.labels[params[0]], 0, 0))
            if line.startswith("RET"):
                self.bytecode.append(self.get_hex(13, 0, 0, 0))
            if line.startswith("PUSH"):
                self.bytecode.append(self.get_hex(14, self.variables[params[0]], 0, 0))
            if line.startswith("POP"):
                self.bytecode.append(self.get_hex(15, self.variables[params[0]], 0, 0))

            if line.startswith("END"):
                self.bytecode.append(self.get_hex(255, 0, 0, 0))

    def read_file(self):
        with open("fib-rec2.in", 'r') as in_stream:
            self.code = [line.strip() for line in in_stream.readlines()]

    def write_file(self):
        with open('fib.out', 'w') as out_stream:
            for line in self.bytecode:
                out_stream.write(line + '\n')

assembler = Assembler()
assembler.run()
