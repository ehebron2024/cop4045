"""
Problem 2 - List and Dictionary Comprehensions
Replace 'Lastname_Firstname' in the filename with your own last and first name
before submitting (e.g., p2_Smith_John.py).
"""

# ---------------------------------------------------------------------------
# a) All tuples (a, b, c, d) with a, b, c, d distinct integers, 1 <= a,b,c,d <= 10,
#    such that a^2 + b^2 = c^2 + d^2
# ---------------------------------------------------------------------------
pythagorean_like = [
    (a, b, c, d)
    for a in range(1, 11)
    for b in range(1, 11)
    for c in range(1, 11)
    for d in range(1, 11)
    if len({a, b, c, d}) == 4 and a**2 + b**2 == c**2 + d**2
]

print("a)", pythagorean_like)


# ---------------------------------------------------------------------------
# b) Given a list of strings, produce a list of (lowercase_string, length) tuples
#    for strings whose length is strictly shorter than 5 characters.
# ---------------------------------------------------------------------------
words_b = ['One', 'SEVEN', 'three', 'two', 'Ten']

lower_short = [
    (word.lower(), len(word))
    for word in words_b
    if len(word) < 5
]

print("b)", lower_short)


# ---------------------------------------------------------------------------
# c) Given full names "Firstname Middlename Lastname", produce
#    "Firstname M. Lastname"
# ---------------------------------------------------------------------------
names = ['Eden Rebecca Hebron', 'Nicole Jill Cook']

abbreviated_names = [
    f"{name.split()[0]} {name.split()[1][0]}. {name.split()[2]}"
    for name in names
]

print("c)", abbreviated_names)


# ---------------------------------------------------------------------------
# d) Given two lists of strings, find all pairs (w1, w2) with w1 from lst1
#    and w2 from lst2 that are anagrams of each other (case insensitive).
# ---------------------------------------------------------------------------
lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]

anagram_pairs = [
    (w1, w2)
    for w1 in lst1
    for w2 in lst2
    if sorted(w1.lower()) == sorted(w2.lower())
]

print("d)", anagram_pairs)


# ---------------------------------------------------------------------------
# e) Given a list of distinct strings, map each string to its length.
# ---------------------------------------------------------------------------
s = ['one', 'two', 'three']

string_lengths = {word: len(word) for word in s}
print("e)", string_lengths)
text = "Hello world"

vowel_indices = {
    i: c
    for i, c in enumerate(text)
    if c.lower() in "aeiou"
}

print("f)", vowel_indices)
print("Ehebron2024")