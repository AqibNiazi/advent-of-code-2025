import sys
from typing import List, Tuple, Set


def parse_ranges(text: str) -> List[Tuple[int, int]]:
    """
    Parse comma-separated ranges like '11-22,95-115,...' into a list of (a, b).
    Only keeps ranges where a <= b.
    """
    text = text.replace("\n", "")
    parts = text.split(",")
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


def repeated_number_from_base(x: int, k: int, m: int) -> int:
    """
    Construct the integer formed by repeating the k-digit number x exactly m times.
    Example: x=123, k=3, m=2 -> 123123
    """
    return int(str(x) * m)


def generate_repeateds_in_range(a: int, b: int) -> Set[int]:
    """
    Generate all integers n in [a, b] that are repetitions of some base X
    repeated m >= 2 times. Return them as a set to avoid duplicates.

    Strategy:
      - Let max_len be number of digits of b.
      - For base length k from 1 to max_len//2:
          For repetition m from 2 while k*m <= max_len:
              Compute bounds for X using factor M = (10^(k*m)-1)//(10^k-1).
              Iterate allowed X values, build n = repeat(X, k, m).
      - Collect n in a set to deduplicate across different (k, m).
    """
    results = set()
    max_len = len(str(b))

    for k in range(1, max_len + 1):
        # Stop if even m=2 would exceed max_len digits
        if 2 * k > max_len:
            break

        pow10_k = 10 ** k
        m = 2

        while k * m <= max_len:
            # Multiplier for constructing repeated numbers
            pow10_km = 10 ** (k * m)
            M = (pow10_km - 1) // (pow10_k - 1)

            # Bounds for X based on range constraints
            x_min_val = (a + M - 1) // M  # ceil(a / M)
            x_max_val = b // M            # floor(b / M)

            # Bounds for X based on digit length (k-digit, no leading zeros)
            x_min_digits = 10 ** (k - 1)
            x_max_digits = 10 ** k - 1

            # Final valid range for X
            low = max(x_min_val, x_min_digits)
            high = min(x_max_val, x_max_digits)

            if low <= high:
                for X in range(low, high + 1):
                    n = repeated_number_from_base(X, k, m)
                    if a <= n <= b:
                        results.add(n)

            m += 1

    return results


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
        reps = generate_repeateds_in_range(a, b)
        grand_total += sum(reps)

    print(grand_total)


if __name__ == "__main__":
    main()