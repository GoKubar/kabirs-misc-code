image = {}
for a in range(1, 21):
    for b in range(1, 21):
        y = (a + 1) * (a + 2 * b) // 2
        if y <= 20:
            image[y] = (a, b)

for k in sorted([k for k in image]):
    print(k, image[k])
