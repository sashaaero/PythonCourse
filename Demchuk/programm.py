from PIL import ImageDraw, ImageFont, Image
Text = str(input())


font = ImageFont.truetype('arialbd.ttf', 15) #load the font
size = font.getsize(Text)  #size = size_text
image = Image.new('1', size, 1)  #white/black picture
draw = ImageDraw.Draw(image)
draw.text((0, 0), Text, font=font) #draw text in image


def BitToChar(self, col, row):
    if self.getpixel((col, row)):
        return ' '
    else:
        return 'X'

for r in range(size[1]):
    print(''.join([BitToChar(image, c, r) for c in range(size[0])]))