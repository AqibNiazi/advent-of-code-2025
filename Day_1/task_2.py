from typing import Iterable


def parse_instruction(line: str):
    """
    Parse a single rotation instruction.
    Accepts formats like 'L68' or 'R 48'.
    Returns (direction, distance) or None if invalid.
    """
    s = line.strip()
    if not s:
        return None

    # Compact form: "L68"
    if s[0] in ('L', 'R') and s[1:].strip().lstrip('+-').isdigit():
        return s[0], int(s[1:].strip())

    # Spaced form: "L 68"
    parts = s.split()
    if len(parts) == 2 and parts[0] in ('L', 'R') and parts[1].lstrip('+-').isdigit():
        return parts[0], int(parts[1])

    return None


def hits_on_zero_during_rotation(start_pos: int, direction: str, distance: int) -> int:
    """
    Count how many times the dial equals 0 during a single rotation.
    Checks each click from 1..distance starting at start_pos.
    """
    if distance <= 0:
        return 0

    if direction == 'R':
        # First click that lands on 0 when rotating right
        k0 = (100 - start_pos) % 100
    else:  # 'L'
        # First click that lands on 0 when rotating left
        k0 = start_pos % 100

    # Interpret k0 == 0 as the 100th click
    if k0 == 0:
        k0 = 100

    if distance < k0:
        return 0

    # First hit at k0, then every +100 clicks
    return 1 + (distance - k0) // 100


def count_zero_hits(lines: Iterable[str]) -> int:
    """
    Process all instructions and count total hits on 0
    across the entire sequence of rotations.
    """
    pos = 50  # starting position
    total_hits = 0

    for raw in lines:
        parsed = parse_instruction(raw)
        if not parsed:
            continue

        direction, dist = parsed

        # Count hits during this rotation
        total_hits += hits_on_zero_during_rotation(pos, direction, dist)

        # Update dial position after rotation
        if direction == 'R':
            pos = (pos + dist) % 100
        else:
            pos = (pos - dist) % 100

    return total_hits


def read_input_file(path: str = "input.txt") -> list[str]:
    """
    Read input lines from file.
    Default file is 'input.txt' in current folder.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Error: '{path}' not found in the current folder.", flush=True)
        return []


def main():
    """
    Entry point: read input, run simulation, print result.
    """
    lines = read_input_file("input.txt")
    if not lines:
        return

    result = count_zero_hits(lines)
    print(result)


if __name__ == "__main__":
    main()