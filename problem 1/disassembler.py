__author__ = 'Alexander Demidov'

COMMAND_MASK = 0xFF000000

#системные регистры
IP_POS = 0
COMPARISON_FLAG_POS = 1
SP_POS = 2
CUR_COMMAND_POS = 3
SRC_ARG_POS = 4
DST_ARG_POS = 5
WORK_STATUS_POS = 6

COMMAND_TABLE = {
    -1: "NONE",
    255: "END",
    1: "SUB",
    2: "MOV",
    3: "ADD",
    4: "CMP",
    5: "OUT",
    6: "IN",
    7: "JNQ",
    8: "JL",
    9: "JQ",
    10: "JG",
    11: "JMP",
    12: "CALL",
    13: "RET",
    14: "PUSH",
    15: "POP"
}

ARGS_TABLE = {
    "NONE": {"src_mask": 0, "src_shift": 0, "dst_mask": 0, "dst_shift": 0},
    "END": {"src_mask": 0x00FF0000, "src_shift": 16, "dst_mask": 0, "dst_shift": 0},

    "MOV": {"src_mask": 0x00FF0000, "src_shift": 16, "dst_mask": 0x0000FF00, "dst_shift": 8},
    "ADD": {"src_mask": 0x00FF0000, "src_shift": 16, "dst_mask": 0x0000FF00, "dst_shift": 8},
    "SUB": {"src_mask": 0x00FF0000, "src_shift": 16, "dst_mask": 0x0000FF00, "dst_shift": 8},

    "OUT": {"src_mask": 0x00FF0000, "src_shift": 16, "dst_mask": 0, "dst_shift": 0},
    "IN": {"src_mask": 0, "src_shift": 0, "dst_mask": 0x00FF0000, "dst_shift": 16},

    "JNQ": {"src_mask": 0, "src_shift": 0, "dst_mask": 0x00FF0000, "dst_shift": 16},
    "JQ": {"src_mask": 0, "src_shift": 0, "dst_mask": 0x00FF0000, "dst_shift": 16},
    "JG": {"src_mask": 0, "src_shift": 0, "dst_mask": 0x00FF0000, "dst_shift": 16},
    "JL": {"src_mask": 0, "src_shift": 0, "dst_mask": 0x00FF0000, "dst_shift": 16},
    "JMP": {"src_mask": 0, "src_shift": 0, "dst_mask": 0x00FF0000, "dst_shift": 16},

    "CMP": {"src_mask": 0x00FF0000, "src_shift": 16, "dst_mask": 0x0000FF00, "dst_shift": 8},

    "CALL": {"src_mask": 0, "src_shift": 0, "dst_mask": 0x00FF0000, "dst_shift": 16},
    "RET": {"src_mask": 0x00FF0000, "src_shift": 16, "dst_mask": 0, "dst_shift": 0},
    "PUSH": {"src_mask": 0x00FF0000, "src_shift": 16, "dst_mask": 0, "dst_shift": 0},
    "POP": {"src_mask": 0, "src_shift": 0, "dst_mask": 0x00FF0000, "dst_shift": 16}
}


class Disassembler:
    def __init__(self):
        self.code = []
        self.disassembled_code = []
        self.labels = {}

    def run(self):
        self.read_code()

        self.code[CUR_COMMAND_POS] = "NONE"
        self.code[SRC_ARG_POS] = 0
        self.code[DST_ARG_POS] = 0
        self.code[WORK_STATUS_POS] = True

        for variable_number in range(self.code[IP_POS] - 7):
            self.add_variable(variable_number, self.code[variable_number + 7])

        while self.code[IP_POS] < len(self.code):
            self.decode_command()
            self.decode_arguments()
            self.process()
            self.code[IP_POS] += 1

        self.add_labels()
        self.write_file()

    def read_code(self):
        with open("fib.out") as in_stream:
            self.code = [int(x, 16) for x in in_stream.readlines()]

    def write_file(self):
        with open('fib.dis', 'w') as out_stream:
            for line in self.disassembled_code:
                out_stream.write(line + '\n')

    def add_variable(self, variable_number, value):
        self.disassembled_code.append("LET var" + str(variable_number) + " " + str(value))

    def add_command(self, command_name, *args, param_type="var"):
        if len(args) == 0:
            self.disassembled_code.append(str(command_name))
        elif len(args) == 1:
            if param_type == " label":
                label_name = "label" + str(args[0] - 7)
                self.labels[str(args[0] - 7)] = label_name
            self.disassembled_code.append(str(command_name) + param_type + str(args[0] - 7))
        elif len(args) == 2:
            self.disassembled_code.append(str(command_name) + " var" + str(args[0] - 7) + " var" + str(args[1] - 7))

    def add_labels(self):
        for label in sorted(self.labels.keys())[::-1]:
            self.disassembled_code = self.disassembled_code[:int(label)] \
                + [self.labels[label] + ":"] + self.disassembled_code[int(label):]

    def decode_command(self):
        self.code[CUR_COMMAND_POS] = COMMAND_TABLE[(self.code[self.code[IP_POS]] & COMMAND_MASK) >> 24]

    def decode_arguments(self):
        self.code[SRC_ARG_POS] = (self.code[self.code[IP_POS]] & ARGS_TABLE[self.code[CUR_COMMAND_POS]]["src_mask"])
        self.code[SRC_ARG_POS] >>= ARGS_TABLE[self.code[CUR_COMMAND_POS]]["src_shift"]

        self.code[DST_ARG_POS] = (self.code[self.code[IP_POS]] & ARGS_TABLE[self.code[CUR_COMMAND_POS]]["dst_mask"])
        self.code[DST_ARG_POS] >>= ARGS_TABLE[self.code[CUR_COMMAND_POS]]["dst_shift"]

    def process(self):
        if self.code[CUR_COMMAND_POS] == "MOV":
            self.add_command("MOV", self.code[SRC_ARG_POS], self.code[DST_ARG_POS])
        elif self.code[CUR_COMMAND_POS] == "ADD":
            self.add_command("ADD", self.code[SRC_ARG_POS], self.code[DST_ARG_POS])
        elif self.code[CUR_COMMAND_POS] == "SUB":
            self.add_command("SUB", self.code[SRC_ARG_POS], self.code[DST_ARG_POS])

        elif self.code[CUR_COMMAND_POS] == "OUT":
            self.add_command("OUT", self.code[SRC_ARG_POS], param_type=" var")
        elif self.code[CUR_COMMAND_POS] == "IN":
            self.add_command("IN", self.code[DST_ARG_POS], param_type=" var")

        elif self.code[CUR_COMMAND_POS] == "CALL":
            self.add_command("CALL", self.code[DST_ARG_POS], param_type=" label")
        elif self.code[CUR_COMMAND_POS] == "RET":
            self.add_command("RET")
        elif self.code[CUR_COMMAND_POS] == "PUSH":
            self.add_command("PUSH", self.code[SRC_ARG_POS], param_type=" var")
        elif self.code[CUR_COMMAND_POS] == "POP":
            self.add_command("POP", self.code[DST_ARG_POS], param_type=" var")

        elif self.code[CUR_COMMAND_POS] == "JNQ":
            self.add_command("JNQ", self.code[DST_ARG_POS], param_type=" label")
        elif self.code[CUR_COMMAND_POS] == "JQ":
            self.add_command("JQ", self.code[DST_ARG_POS], param_type=" label")
        elif self.code[CUR_COMMAND_POS] == "JG":
            self.add_command("JG", self.code[DST_ARG_POS], param_type=" label")
        elif self.code[CUR_COMMAND_POS] == "JL":
            self.add_command("JL", self.code[DST_ARG_POS], param_type=" label")
        elif self.code[CUR_COMMAND_POS] == "JMP":
            self.add_command("JMP", self.code[DST_ARG_POS], param_type=" label")

        elif self.code[CUR_COMMAND_POS] == "CMP":
            self.add_command("CMP", self.code[SRC_ARG_POS], self.code[DST_ARG_POS])

        elif self.code[CUR_COMMAND_POS] == "END":
            self.add_command("END")
            self.code[WORK_STATUS_POS] = False

disassembler = Disassembler()
disassembler.run()
