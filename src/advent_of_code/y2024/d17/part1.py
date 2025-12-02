from collections import defaultdict
from common.input import input, compile

reg_pattern = compile("Register <str>: <int>")

registers = defaultdict(int)
lines = input()
for line in lines:
    if line == "":
        break
    char, value = reg_pattern(line)
    registers[char] = value

program = list(map(lambda x: int(x, 8), next(lines).split(": ")[1].split(",")))


print(registers)
print(program)


# The adv instruction (opcode 0) performs division. The numerator is the value
# in the A register. The denominator is found by raising 2 to the power of the
# instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2);
# an operand of 5 would divide A by 2^B.) The result of the division operation
# is truncated to an integer and then written to the A register.
def adv(a, b, c, lit_operand, cmb_operand):
    numerator = a
    denominator = 2**cmb_operand
    a = numerator // denominator
    return None, a, b, c, None


# The bxl instruction (opcode 1) calculates the bitwise XOR of register B and
# the instruction's literal operand, then stores the result in register B.
def bxl(a, b, c, lit_operand, cmb_operand):
    b = b ^ lit_operand
    return None, a, b, c, None


# The bst instruction (opcode 2) calculates the value of its combo operand
# modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to
# the B register.
def bst(a, b, c, lit_operand, cmb_operand):
    b = cmb_operand & 0b111
    return None, a, b, c, None


# The jnz instruction (opcode 3) does nothing if the A register is 0. However,
# if the A register is not zero, it jumps by setting the instruction pointer to
# the value of its literal operand; if this instruction jumps, the instruction
# pointer is not increased by 2 after this instruction.
def jnz(a, b, c, lit_operand, cmb_operand):
    if a == 0:
        return None, a, b, c, None
    return lit_operand, a, b, c, None


# The bxc instruction (opcode 4) calculates the bitwise XOR of register B and
# register C, then stores the result in register B. (For legacy reasons, this
# instruction reads an operand but ignores it.)
def bxc(a, b, c, lit_operand, cmb_operand):
    b = b ^ c
    return None, a, b, c, None


# The out instruction (opcode 5) calculates the value of its combo operand
# modulo 8, then outputs that value. (If a program outputs multiple values,
# they are separated by commas.)
def out(a, b, c, lit_operand, cmb_operand):
    mod8 = cmb_operand & 0b111
    return None, a, b, c, str(mod8)


# The bdv instruction (opcode 6) works exactly like the adv instruction except
# that the result is stored in the B register. (The numerator is still read
# from the A register.)
def bdv(a, b, c, lit_operand, cmb_operand):
    numerator = a
    denominator = 2**cmb_operand
    b = numerator // denominator
    return None, a, b, c, None


# The cdv instruction (opcode 7) works exactly like the adv instruction except
# that the result is stored in the C register. (The numerator is still read
# from the A register.)
def cdv(a, b, c, lit_operand, cmb_operand):
    numerator = a
    denominator = 2**cmb_operand
    c = numerator // denominator
    return None, a, b, c, None


opcodes = {
    0o0: adv,
    0o1: bxl,
    0o2: bst,
    0o3: jnz,
    0o4: bxc,
    0o5: out,
    0o6: bdv,
    0o7: cdv,
}


def compute(a, b, c, opcode, lit_operand):
    if lit_operand == 0o4:
        cmb_operand = a
    elif lit_operand == 0o5:
        cmb_operand = b
    elif lit_operand == 0o6:
        cmb_operand = c
    elif lit_operand == 0o7:
        raise ValueError("Invalid operand")
    else:
        cmb_operand = lit_operand

    return opcodes[opcode](a, b, c, lit_operand, cmb_operand)


# assert compute(0, 0, 9, 2, 6) == (None, 0, 1, 9, None)
# assert compute(10, 0, 0, 5, 0) == (None, 10, 0, 0, "0")
# assert compute(10, 0, 0, 5, 1) == (None, 10, 0, 0, "1")
# assert compute(10, 0, 0, 5, 4) == (None, 10, 0, 0, "2")
# assert compute(2024, 0, 0, 0, 1) == (None, 1012, 0, 0, None)
# assert compute(1012, 0, 0, 5, 4) == (None, 1012, 0, 0, "4")
# assert compute(1012, 0, 0, 3, 0) == (0, 1012, 0, 0, None)

instruction_pointer = 0
a, b, c = (registers["A"], registers["B"], registers["C"])
output = []
while instruction_pointer < len(program):
    opcode = program[instruction_pointer]
    operand = program[instruction_pointer + 1]
    jmp, a, b, c, out = compute(a, b, c, opcode, operand)
    if jmp is not None:
        instruction_pointer = jmp
    else:
        instruction_pointer += 2
    if out is not None:
        output.append(out)

print(",".join(output))
