import argparse
import json
import sys

import PIL.ImageFont

from . import char2image


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('document_file', nargs='?',
                        type=argparse.FileType(), default=sys.stdin)
    parser.add_argument('-s', '--size', type=int, default=32)
    parser.add_argument('-f', '--font-file', required=True)
    return parser.parse_args()


def main():
    args = get_args()

    print(json.dumps(
        char2image.chars_to_images(
            {char for char in args.document_file.read()},
            PIL.ImageFont.truetype(args.font_file, size=int(args.size))),
        ensure_ascii=False))


if __name__ == '__main__':
    main()
