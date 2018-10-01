from PIL import Image

img = Image.open("image.png").convert("RGBA")
frame = Image.open("frame.png").convert("RGBA")
out = Image.new('RGBA', (512, 874), color=255)
class_i = Image.open("class.png").convert("RGBA")
x, y = out.size
out.paste(img,(0, 30), img)
out.paste(frame,(0, 0, x, y), frame)
out.paste(class_i,(217, 770), class_i)
out.save("out.png", format="png")
out.show()

