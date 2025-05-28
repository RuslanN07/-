import re

def is_palindrome(s): return s == s[::-1

num_words = {'0': 'ноль', '1': 'один', '2': 'два', '3': 'три'}

pattern = re.compile(r'\b([0123]+)\b')

with open("1lab.txt") as f:
    data = f.read()

for n in pattern.findall(data):
    if len(n) > 1 and n[-2] == '1' and n[-1] in '13':
        dec = int(n, 4)
        if dec <= 1023 and dec % 2:
            print(" ".join(num_words[c] for c in n) if is_palindrome(n) else n[::-1])
