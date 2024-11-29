from PIL import Image
from model import imagetob64

img = Image.open("./test.jpeg")

print(imagetob64(img))
