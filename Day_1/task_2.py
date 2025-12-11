#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 1 Part 2 (method 0x434C49434B)

Reads rotations from input.txt (same folder) and counts how many times
the dial points at 0 during the entire sequence of clicks (including
intermediate clicks and the final click of each rotation).

Dial numbers: 0..99, starts at 50.
"""

from typing import Iterable

def parse_line(line: str):
    """Return (direction, distance) or None for invalid line."""
    s = line.strip()
    if not s:
        return None
    # Accept "L68", "R48", or "L 68", "R 48"
    if s[0] in ('L', 'R') and s[1:].strip().lstrip('+-').isdigit():
        return s[0], int(s[1:].strip())
    parts = s.split()
    if len(parts) == 2 and parts[0] in ('L', 'R') and parts[1].lstrip('+-').isdigit():
        return parts[0], int(parts[1])
    return None

def hits_on_zero_during_rotation(start_pos: int, direction: str, distance: int) -> int:
    """
    Count how many times the dial equals 0 for clicks k=1..distance,
    when starting at start_pos (0..99).
    """
    if distance <= 0:
        return 0

    if direction == 'R':
        # We need k in [1..d] such that (start_pos + k) % 100 == 0
        k0 = (100 - start_pos) % 100  # first k that hits 0 (0..99)
    else:  # 'L'
        # We need k in [1..d] such that (start_pos - k) % 100 == 0
        k0 = start_pos % 100  # first k that hits 0 (0..99)

    # interpret k0==0 as the 100th click (i.e., every 100 clicks)
    if k0 == 0:
        k0 = 100

    if distance < k0:
        return 0
    # first hit at k0, then every +100
    return 1 + (distance - k0) // 100

def count_zero_hits_from_lines(lines: Iterable[str]) -> int:
    pos = 50
    total_hits = 0

    for raw in lines:
        parsed = parse_line(raw)
        if parsed is None:
            continue
        direction, dist = parsed

        # count hits during this rotation (k = 1..dist)
        total_hits += hits_on_zero_during_rotation(pos, direction, dist)

        # update position to end of rotation
        if direction == 'R':
            pos = (pos + dist) % 100
        else:
            pos = (pos - dist) % 100

    return total_hits

def main():
    try:
        with open("input.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: 'input.txt' not found in the current folder.", flush=True)
        return

    result = count_zero_hits_from_lines(lines)
    print(result)

if __name__ == "__main__":
    main()
