from PIL import Image
import random


def gen_logo():
    size = 8

    b = []

    for i in range(size):
        b.append('')
        for _ in range(size // 2):
            x = str(random.randint(0, 1))
            b[i] = b[i] + x
        b[i] = b[i] + b[i][::-1]


    im = Image.new("L", (size, size))
    data = im.load()
    for x in range(len(b)):
        for y in range(len(b[x])):
            data[y, x] = int(b[x][y]) * 255
    im.load()

    return im

im = gen_logo()
im.save('logo.png',"PNG")