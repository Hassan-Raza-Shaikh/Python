# Lab #03: Rate Limited Hashtag Timelines

# -----------------------------------------------
# Set your own registration number here
REG = "2024017"  # <-- change this to your own registration number
# -----------------------------------------------

def compute_limits(REG):
    """Compute m, n, k from registration number."""
    digits = [int(d) for d in REG]
    last = digits[-1]
    second_last = digits[-2] if len(digits) > 1 else 0
    m = last + 1
    n = (sum(digits) % 3) + 1
    k = (second_last % 4) + 2
    return m, n, k


def valid_alphabet(timeline):
    """Check that timeline only has #, _, or !"""
    for ch in timeline:
        if ch not in "#_!":
            return False
    return True


def bang_cap_ok(timeline, k):
    """Check that no run of ! exceeds k."""
    count = 0
    for ch in timeline:
        if ch == '!':
            count += 1
            if count > k:
                return False
        else:
            count = 0
    return True


def count_hashtag_blocks(timeline):
    """Return list of (start, end) indices of hashtag blocks."""
    blocks = []
    i = 0
    while i < len(timeline):
        if timeline[i] == '#':
            start = i
            while i < len(timeline) and timeline[i] == '#':
                i += 1
            end = i - 1
            blocks.append((start, end))
        else:
            i += 1
    return blocks


def cool_down_ok(timeline, blocks, n):
    """Check underscore requirement between consecutive hashtag blocks."""
    for i in range(len(blocks) - 1):
        end_prev = blocks[i][1]
        start_next = blocks[i + 1][0]
        segment = timeline[end_prev + 1:start_next]
        underscore_run = 0
        satisfied = False
        for ch in segment:
            if ch == '_':
                underscore_run += 1
                if underscore_run >= n:
                    satisfied = True
            elif ch == '!':
                underscore_run = 0  # reset on !
        if not satisfied:
            return False
    return True


def evaluate_timeline(timeline, m, n, k):
    """Return ACCEPT or REJECT for one timeline."""
    if not valid_alphabet(timeline):
        return "REJECT"
    if not bang_cap_ok(timeline, k):
        return "REJECT"

    blocks = count_hashtag_blocks(timeline)
    if len(blocks) > m:
        return "REJECT"
    if len(blocks) <= 1:
        # No cooldown rule needed
        return "ACCEPT"
    if not cool_down_ok(timeline, blocks, n):
        return "REJECT"
    return "ACCEPT"


def main():
    import sys
    m, n, k = compute_limits(REG)
    for line in sys.stdin:
        timeline = line.strip()
        if not timeline:
            continue  # ignore empty lines
        print(evaluate_timeline(timeline, m, n, k))


if __name__ == "__main__":
    main()