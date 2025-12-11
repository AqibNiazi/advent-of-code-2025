from typing import List, Tuple
import sys


def parse_ranges(text: str) -> List[Tuple[int, int]]:
    """
    Parse comma-separated ranges like '11-22,95-115,...' into a list of (a, b).
    Only keeps ranges where a <= b.
    """
    parts = text.replace("\n", "").split(",")
    ranges = []

    for p in parts:
        p = p.strip()
        if not p or "-" not in p:
            continue

        a_str, b_str = p.split("-", 1)
        a, b = int(a_str), int(b_str)

        if a <= b:
            ranges.append((a, b))

    return ranges


def sum_double_numbers_in_range(a: int, b: int) -> int:
    """
    Sum all numbers n in [a, b] that are of the form XX,
    where X is a k-digit number without leading zeros (k >= 1).
    Representation: n = X * (10^k + 1).
    """
    total = 0
    len_b = len(str(b))
    max_k = len_b // 2  # maximum possible k based on digit length of b

    for k in range(1, max_k + 1):
        M = 10**k + 1  # multiplier for constructing XX

        # Bounds for X based on range constraints
        x_min_val = -(-a // M)       # ceil(a / M)
        x_max_val = b // M           # floor(b / M)

        # Bounds for X based on digit length (k-digit, no leading zeros)
        x_min_digits = 10**(k - 1)
        x_max_digits = 10**k - 1

        # Final valid range for X
        low = max(x_min_val, x_min_digits)
        high = min(x_max_val, x_max_digits)

        if low <= high:
            count = high - low + 1
            # Arithmetic series sum of X values
            sum_X = (low + high) * count // 2
            total += sum_X * M

    return total


def read_input_file(path: str = "input.txt") -> str:
    """
    Read the entire input file as a string.
    Default file is 'input.txt' in current folder.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: '{path}' not found in current folder.", file=sys.stderr)
        sys.exit(1)


def main():
    """
    Entry point: read input, parse ranges, compute grand total.
    """
    text = read_input_file("input.txt")
    ranges = parse_ranges(text)

    grand_total = 0
    for a, b in ranges:
        grand_total += sum_double_numbers_in_range(a, b)

    print(grand_total)


if __name__ == "__main__":
    main()