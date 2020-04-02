#Given a string, find the first non-repeating character in it and return it's index. If it doesn't exist, return -1.
def finduniquechar(s):
    unique = {}
    k = unique.keys()
    for ch in range(len(s)):
        if s[ch] not in k:
            unique[s[ch]] = ch
        else:
            unique[s[ch]] = -1
    v = unique.values()
    v = [i for i in v if i != -1]
    if not v:
        return -1
    return sorted(v)[0]
finduniquechar("cc")
