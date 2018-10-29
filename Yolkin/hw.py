n = int(input())
p = int(input())
d = (100 - p) / n
d_20 = d / 2
if p > 20:
    t = (p - 20) / d + 20 / d_20
elif p < 20:
    t = p / d_20
print(t)