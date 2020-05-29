"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
PRA = 0b01001000

SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8

    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def load(self, filename):
        print(filename)
        """Load a program into memory."""
        try:
            address = 0
            # Open the file
            with open(filename) as f:
                # Read all the lines
                for line in f:
                    # Parse out comments
                    comment_split = line.strip().split("#")
                    # Cast the numbers from strings to ints
                    value = comment_split[0].strip()
                    # Ignore blank lines
                    if value == "":
                        continue

                    num = int(value, 2)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    if len(sys.argv) != 2:
        print("ERROR: Must have file name")
        sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def run(self):
        """Run the CPU."""
        while True:
            # print(f'Ram: {self.ram}')
            print(f"Register: {self.reg}")
            opcode = self.ram[self.pc]
            # print(f'Opcode: {opcode}')
            # print(f'Opcode: {opcode}')
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if opcode == LDI:
                # print('LDI')
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif opcode == PRN:
                # print('PRN')
                print(self.reg[operand_a])
                self.pc += 2
            elif opcode == MUL:
                # print('MUL')
                product = self.reg[operand_a] * self.reg[operand_b]
                print(product)
                self.pc += 3
            elif opcode == PUSH:
                # print('PUSH')
                val = self.reg[operand_a]
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = val
                self.pc += 2
            elif opcode == POP:
                # print('POP')
                val = self.ram[self.reg[SP]]
                self.reg[operand_a] = val
                self.reg[SP] += 1
                self.pc += 2
            elif opcode == CALL:
                # print('CALL')
                val = self.pc + 2
                reg = self.ram[self.pc + 1]
                sub = self.reg[reg]
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = val
                self.pc = sub
            elif opcode == RET:
                # print('RET')
                ret = self.reg[SP]
                self.pc = self.ram[ret]
                self.reg[SP] += 1
            elif opcode == ADD:
                # print('ADD')
                self.reg[operand_a] += self.reg[operand_b]
                self.pc += 3
            elif opcode == PRA:
                # print('PRA')
                # Print alpha character value stored in the given register.
                print("alpha character", self.reg[self.ram[self.pc + 1]])
                # Print to the console the ASCII character corresponding to the value in the register.
                print("ASCII", chr(self.reg[self.ram[self.pc + 1]]))
                self.pc += 2
            elif opcode == HLT:
                print("HLT")
                sys.exit(0)
            else:
                print(f"I did not understand that command: {opcode}")
                sys.exit(1)
