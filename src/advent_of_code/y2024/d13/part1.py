from common.input import input, compile
from common.space import Space, adjacent4

a_pattern = compile("Button A: X+<int>, Y+<int>")
b_pattern = compile("Button B: X+<int>, Y+<int>")
prize_pattern = compile("Prize: X=<int>, Y=<int>")

machines = []
for line in input():
    if line.startswith("Button A"):
        a_move = a_pattern(line)
    if line.startswith("Button B"):
        b_move = b_pattern(line)
    if line.startswith("Prize"):
        prize = prize_pattern(line)
        machines.append((a_move, b_move, prize))

total = 0
for machine in machines:
    print(machine)
    (ax, ay), (bx, by), (px, py) = machine

    B = (ay * px - ax * py) / (ay * bx - ax * by)
    A = (px - B * bx) / ax

    if A.is_integer() and B.is_integer():
        print(f"Found: A={A}, B={B}")
        total += 3 * int(A) + int(B)

print(total)
