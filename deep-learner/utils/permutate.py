def permutate(counts):
    permutatations = []
    ranks = []

    def build(lists, prefix=[]):
        if not lists:
            permutatations.append(tuple(prefix))
            return
        first = lists[0]
        rest = lists[1:]
        for item in first:
            build(rest, prefix + [item])

    for count in counts:
        amount = list(range(count + 1))
        ranks.append(amount)

    build(ranks)
    return permutatations


def compress(permutations):
    compressed = []
    start = 0
    for count in counts:
        items = permutations[start : start + count]
        filtered = list(filter(lambda played: played == 1, list(items)))
        compressed.append(len(filtered))
        start += count
    return tuple(compressed)
