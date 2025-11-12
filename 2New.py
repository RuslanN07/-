import re

def is_palindrome(s):
    return s == s[::-1]

num_words = {'0': 'ноль', '1': 'один', '2': 'два', '3': 'три'}

# ЗАХВАТЫВАЕМ ВСЁ ЧИСЛО, если оно заканчивается на 1[13]
pattern = re.compile(r'\b([0123]+1[13])\b')

with open("2L.txt", encoding="utf-8") as f:
    data = f.read()

for n in pattern.findall(data):
    dec = int(n, 4)
    if dec <= 1023 and dec % 2 == 1:
        if is_palindrome(n):
            print(" ".join(num_words[c] for c in n))
        else:
            print(n[::-1])