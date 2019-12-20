"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8 # like vars
        self.ram = [0] * 256
        self.pc = 0
        self.fl = 0
        """
        self.mar = 0 
        self.mdr = 0
        """
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
    
    def filter_comment(self, line):
        if line[0] == '#' or line[0] == "\n":
            return False
        else:
            return True

    def load(self, file_location):
        """Load a program into memory."""
        program_to_run = []
        with open(file_location) as file:
            program = file.readlines()

        program_fil = list(filter(self.filter_comment, program))
        for line_exc in program_fil:
            head, sep, tail = line_exc.partition('#')
            program_to_run.append(int(head,2))

        address = 0

        for instruction in program_to_run:
            self.ram[address] = instruction
            address += 1

    def run(self):
        """Run the CPU."""
        IR = self.pc
        halted = False
        self.reg[7] = 0xF4
        SP = self.reg[7]

        while not halted:
            operand_a = self.ram_read(IR+1)
            operand_b = self.ram_read(IR+2)
            instruction = self.ram[IR]

            if instruction == 0x82: #LDI
                self.reg[operand_a] = operand_b
                IR += 3

            elif instruction == 0x47: #PRN
                value = self.reg[operand_a]
                print(value)
                IR += 2

            elif instruction == 0xA2: #MULT
                value = self.reg[operand_a] * self.reg[operand_b]
                self.reg[operand_a] = value
                IR += 3
            
            elif instruction == 0xA0: #ADD
                value = self.reg[operand_a] + self.reg[operand_b]
                self.reg[operand_a] = value
                IR += 3

            elif instruction == 0x45: #PUSH
                SP -= 1
                value = self.reg[operand_a]
                self.ram[SP] = value
                IR += 2

            elif instruction == 0x46: #POP
                value = self.ram[SP]
                self.reg[operand_a] = value
                SP += 1
                IR += 2

            elif instruction == 0xA7: #CMP
                a = self.reg[operand_a]
                b = self.reg[operand_b]

                if a == b:
                    self.fl = 0b00000001
                if a < b:
                    self.fl = 0b00000100
                if a > b:
                    self.fl = 0b00000010
                IR += 3

            elif instruction == 0x50: #CALL
                SP -= 1
                self.ram[SP] = IR + 2
                IR = self.reg[operand_a]
            
            elif instruction == 0x11: # RET
                value = self.ram[SP]
                IR = value

            elif instruction == 0b1: #HLT
                halted = True
                IR += 1
                # self.trace()
            
            else:
                print(f"Unknown Instruction at index {IR}")
                print(self.ram[IR])
                sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()