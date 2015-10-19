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

    "SUB": {"src_mask": 0x00FF0000, "src_shift": 16, "dst_mask": 0x0000FF00, "dst_shift": 8},
    "MOV": {"src_mask": 0x00FF0000, "src_shift": 16, "dst_mask": 0x0000FF00, "dst_shift": 8},
    "ADD": {"src_mask": 0x00FF0000, "src_shift": 16, "dst_mask": 0x0000FF00, "dst_shift": 8},

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


class VirtualMachine:
    def __init__(self):
        self.code = []

    def run(self):
        self.read_code()

        self.code[CUR_COMMAND_POS] = "NONE"
        self.code[SRC_ARG_POS] = 0
        self.code[DST_ARG_POS] = 0
        self.code[WORK_STATUS_POS] = True
        self.add_stack()

        while self.code[WORK_STATUS_POS]:
            self.decode_command()
            self.decode_arguments()
            self.process()
            self.code[IP_POS] += 1

    def read_code(self):
        with open("fib.out") as in_stream:
            self.code = [int(x, 16) for x in in_stream.readlines()]

    def add_stack(self):
        self.code += [0] * 65536

    def decode_command(self):
        self.code[CUR_COMMAND_POS] = COMMAND_TABLE[(self.code[self.code[IP_POS]] & COMMAND_MASK) >> 24]

    def decode_arguments(self):
        self.code[SRC_ARG_POS] = (self.code[self.code[IP_POS]] & ARGS_TABLE[self.code[CUR_COMMAND_POS]]["src_mask"])
        self.code[SRC_ARG_POS] >>= ARGS_TABLE[self.code[CUR_COMMAND_POS]]["src_shift"]

        self.code[DST_ARG_POS] = (self.code[self.code[IP_POS]] & ARGS_TABLE[self.code[CUR_COMMAND_POS]]["dst_mask"])
        self.code[DST_ARG_POS] >>= ARGS_TABLE[self.code[CUR_COMMAND_POS]]["dst_shift"]

    def process(self):
        if self.code[CUR_COMMAND_POS] == "MOV":
            self.code[self.code[DST_ARG_POS]] = self.code[self.code[SRC_ARG_POS]]
        elif self.code[CUR_COMMAND_POS] == "ADD":
            self.code[self.code[DST_ARG_POS]] = self.code[self.code[DST_ARG_POS]] + self.code[self.code[SRC_ARG_POS]]
        elif self.code[CUR_COMMAND_POS] == "SUB":
            self.code[self.code[DST_ARG_POS]] = self.code[self.code[DST_ARG_POS]] - self.code[self.code[SRC_ARG_POS]]

        elif self.code[CUR_COMMAND_POS] == "OUT":
            print(self.code[self.code[SRC_ARG_POS]])
        elif self.code[CUR_COMMAND_POS] == "IN":
            self.code[self.code[DST_ARG_POS]] = int(input("Please, input value: "))

        elif self.code[CUR_COMMAND_POS] == "CALL":
            self.code[self.code[SP_POS]] = self.code[IP_POS]
            self.code[SP_POS] += 1
            self.code[IP_POS] = self.code[DST_ARG_POS] - 1
        elif self.code[CUR_COMMAND_POS] == "RET":
            self.code[IP_POS] = self.code[self.code[SP_POS] - 1]
            self.code[SP_POS] -= 1
        elif self.code[CUR_COMMAND_POS] == "PUSH":
            self.code[self.code[SP_POS]] = self.code[self.code[SRC_ARG_POS]]
            self.code[SP_POS] += 1
        elif self.code[CUR_COMMAND_POS] == "POP":
            self.code[self.code[DST_ARG_POS]] = self.code[self.code[SP_POS] - 1]
            self.code[SP_POS] -= 1

        elif self.code[CUR_COMMAND_POS] == "JNQ":
            if self.code[COMPARISON_FLAG_POS] != 0:
                self.code[IP_POS] = self.code[DST_ARG_POS] - 1
        elif self.code[CUR_COMMAND_POS] == "JQ":
            if self.code[COMPARISON_FLAG_POS] == 0:
                self.code[IP_POS] = self.code[DST_ARG_POS] - 1
        elif self.code[CUR_COMMAND_POS] == "JG":
            if self.code[COMPARISON_FLAG_POS] == 2:
                self.code[IP_POS] = self.code[DST_ARG_POS] - 1
        elif self.code[CUR_COMMAND_POS] == "JL":
            if self.code[COMPARISON_FLAG_POS] == 1:
                self.code[IP_POS] = self.code[DST_ARG_POS] - 1
        elif self.code[CUR_COMMAND_POS] == "JMP":
            self.code[IP_POS] = self.code[DST_ARG_POS] - 1

        elif self.code[CUR_COMMAND_POS] == "CMP":
            if self.code[self.code[SRC_ARG_POS]] == self.code[self.code[DST_ARG_POS]]:
                self.code[COMPARISON_FLAG_POS] = 0
            elif self.code[self.code[SRC_ARG_POS]] < self.code[self.code[DST_ARG_POS]]:
                self.code[COMPARISON_FLAG_POS] = 1
            else:
                self.code[COMPARISON_FLAG_POS] = 2

        elif self.code[CUR_COMMAND_POS] == "END":
            self.code[WORK_STATUS_POS] = False

virtual_machine = VirtualMachine()
virtual_machine.run()