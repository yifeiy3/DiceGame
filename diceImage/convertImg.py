from PIL import Image

imlist = ["d1.png", "d2.png", "d3.png", "d4.png", "d5.png", "d6.png"]
for i in range(len(imlist)):
    Image.open(imlist[i]).save("d{0}.bmp".format(i+1))
    
