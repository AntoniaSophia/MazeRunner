import argparse
from PIL import Image


def main():
    # pass the image as command line argument
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'input_file',
        type=str,
        help="The maze as image file"
    )
    parser.add_argument(
        'output_file',
        type=str,
        help="The maze as text file"
    )
    args = parser.parse_args()

    image_path = args.input_file
    text_path = args.output_file

    img = Image.open(image_path)

    # resize the image
    width, height = img.size
    aspect_ratio = height/width
    new_width = 81
    new_height = aspect_ratio * new_width * 1.0
    img = img.resize((new_width, int(new_height)))
    # new size of image
    # print(img.size)

    # convert image to greyscale format
    img = img.convert('L')

    pixels = img.getdata()

    # # replace each pixel with a character from array
    chars = ["1", "0"]
    new_pixels = [chars[pixel//128] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    # split string of chars into multiple strings of length equal to new width and create a list
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width]
                   for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)

    b = ""
    for a in ascii_image.splitlines():
        b += ','.join(a)
        b += '\n'

    # write to a text file.
    with open(text_path, "w") as f:
        f.write(b)


if __name__ == "__main__":
    main()
