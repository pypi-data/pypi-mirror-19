import json

import docopt
import PIL.ImageFont

from . import char2image


def main():
    """
    Usage:
      char2image [-s <size>] -f <font_file> <document_file>
      char2image (-h | --help)

    Outputs a map of character to font image in JSON format.

    Options:
      -f --font-file <font_file>    Specify a TTF font file.
      -s --size <size>              Specify font size. [default: 16]
      -h --help                     Show help.
    """

    args = docopt.docopt(main.__doc__)

    with open(args['<document_file>']) as phile:
        print(json.dumps(
            char2image.chars_to_images(
                {char for char in phile.read()},
                PIL.ImageFont.truetype(args['--font-file'],
                                       size=int(args['--size']))),
            ensure_ascii=False))


if __name__ == '__main__':
    main()
