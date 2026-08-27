"""
Determine whether a string contains a duplicated substring (a substring
that occurs at least twice without overlapping) of a given length.
"""


def find_dup_str(s, n):
    for i in range(len(s) - n + 1):
        candidate = s[i:i + n]
        for j in range(i + n, len(s) - n + 1):
            if candidate == s[j:j + n]:
                return candidate
    return ""


s = input("Enter a string: ")
n = int(input("Enter a substring length: "))
print(find_dup_str(s, n))


def find_max_dup(s):
    for n in range(len(s) // 2, 0, -1):
        dup = find_dup_str(s, n)
        if dup != "":
            return dup
    return ""


s = input("Enter a string: ")
print(find_max_dup(s))