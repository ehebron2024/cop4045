"""
Find all Pythagorean triples (a, b, c) with 0 < a, b, c <= n,
where a**2 + b**2 == c**2.
"""


def find_Pythagorean(n):
    triples = []
    for a in range(1, n + 1):
        for b in range(1, n + 1):
            for c in range(1, n + 1):
                if a**2 + b**2 == c**2:
                    triples.append((a, b, c))
    return triples


n = int(input("Enter a positive integer n: "))
triples = find_Pythagorean(n)

if triples:
    print(f"Pythagorean triples (a, b, c) with 0 < a, b, c <= {n}:")
    for triple in triples:
        print(triple)
else:
    print(f"No Pythagorean triples found with 0 < a, b, c <= {n}.")
