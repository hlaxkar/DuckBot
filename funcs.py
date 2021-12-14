from PIL import Image, ImageOps


def imagesaq(size):

    image1 = Image.open('temp/temp.png')
    width, height = image1.size

    hlen = (int(width // int(size[0]) * int(size[1])) -
            height) // 2 if width > height else 0
    wlen = (int(height // int(size[1]) * int(size[0])) -
            width) // 2 if width < height else 0
    border = (wlen, hlen, wlen, hlen)

    print(border, width, height)
    if border != (0, 0, 0, 0):

        new_image = ImageOps.expand(image1, border=border, fill='black')
        return new_image
    else:
        return image1