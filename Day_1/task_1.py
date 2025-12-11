import sys
import argparse

def parse_instruction(line):
    """
    Parse a single rotation instruction.
    Accepts formats like 'L68' or 'R 48'.
    Returns (direction, distance) or None if invalid.
    """
    line = line.strip()
    if not line:
        return None

    # Case: compact form like "L68"
    if line[0] in ('L', 'R') and line[1:].strip().isdigit():
        return line[0], int(line[1:].strip())

    # Case: spaced form like "L 68"
    parts = line.split()
    if len(parts) == 2 and parts[0] in ('L', 'R') and parts[1].lstrip('+-').isdigit():
        return parts[0], int(parts[1])

    # Ignore invalid lines
    return None


def apply_rotation(pos, direction, distance):
    """
    Rotate the dial left or right by given distance.
    Dial has 100 positions (0–99).
    """
    if direction == 'L':
        return (pos - distance) % 100
    return (pos + distance) % 100


def count_zero_hits(lines):
    """
    Process all instructions and count how many times
    the dial lands exactly on position 0.
    """
    pos = 50  # starting position
    zero_count = 0

    for raw in lines:
        parsed = parse_instruction(raw)
        if not parsed:
            continue

        dir_char, dist = parsed
        pos = apply_rotation(pos, dir_char, dist)

        if pos == 0:
            zero_count += 1

    return zero_count


def read_input_file(path):
    """
    Read input lines from file or stdin.
    Default encoding is UTF-8.
    """
    if path == '-':
        return sys.stdin.readlines()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Error: file '{path}' not found.", file=sys.stderr)
        sys.exit(2)


def main():
    """
    Entry point: parse arguments, read input, run simulation.
    """
    parser = argparse.ArgumentParser(description="Count how many times the dial lands on 0.")
    parser.add_argument('file', nargs='?', default='input.txt',
                        help="Input file with rotations (one per line). Use '-' to read from stdin.")
    args = parser.parse_args()

    lines = read_input_file(args.file)
    result = count_zero_hits(lines)
    print(result)


if __name__ == '__main__':
    main()