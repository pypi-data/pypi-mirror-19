import json

import docopt
import PIL.ImageFont

from . import char2image


def main():
    """
    Usage:
      char2image [-s <size>] [-u <char>] -f <font_file> <character_file>
      char2image (-h | --help)

    Converts a character-per-line file to a list of font images in JSON format.

    Options:
      -f --font-file <file>     Specify a TTF font file.
      -s --size <size>          Specify font size. [default: 16]
      -u --unknown-char <char>  Specify unknown character for fallback. [default: \uFFFD]
      -h --help                 Show help.
    """

    args = docopt.docopt(main.__doc__)

    with open(args['<character_file>']) as phile:
        chars = [line.strip() for line in phile]

    char_to_image = char2image.chars_to_images(
        set(chars),
        PIL.ImageFont.truetype(args['--font-file'],
                               size=int(args['--size'])))

    print(json.dumps([(char_to_image[char]
                       if char in char_to_image else
                       char_to_image[args['--unknown-char']])
                      for char in chars],
                     ensure_ascii=False))


if __name__ == '__main__':
    main()
