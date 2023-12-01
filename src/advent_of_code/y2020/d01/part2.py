#!python3


def findValue(numbers, number_to_find, low, high):
    if high >= low:
        middle = low + (high - low) // 2
        if numbers[middle] == number_to_find:
            return middle
        elif numbers[middle] < number_to_find:
            return findValue(numbers, number_to_find, middle + 1, high)
        else:
            return findValue(numbers, number_to_find, low, middle - 1)
    else:
        return None


with open("input.txt") as f:
    content = f.readlines()

# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x.strip()) for x in content]

content.sort()

for low_idx, low_value in enumerate(content):
    for mid_idx, mid_value in enumerate(content, start=low_idx):
        if mid_idx == len(content):
            continue
        # print(low_idx, low_value, '  ', mid_idx, mid_value)
        high_value = 2020 - low_value - mid_value
        high_idx = findValue(content, high_value, mid_idx, len(content))
        if high_idx != None:
            print(
                low_value,
                "*",
                mid_value,
                "*",
                high_value,
                "=",
                low_value * mid_value * high_value,
            )
