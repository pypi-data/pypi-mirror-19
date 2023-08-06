import argparse
import json
import sys

import PIL.ImageFont

from . import char2image


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('character_file', nargs='?',
                        type=argparse.FileType(), default=sys.stdin)
    parser.add_argument('-s', '--size', type=int, default=32)
    parser.add_argument('-f', '--font-file', required=True)
    parser.add_argument('-u', '--unknown-char', default='\uFFFD')
    return parser.parse_args()


def main():
    args = get_args()

    chars = [line.strip() for line in args.character_file]

    char_to_image = char2image.chars_to_images(
        set(chars),
        PIL.ImageFont.truetype(args.font_file, size=int(args.size)))

    print(json.dumps([(char_to_image[char]
                       if char in char_to_image else
                       char_to_image[args.unknown_char])
                      for char in chars],
                     ensure_ascii=False))


if __name__ == '__main__':
    main()
