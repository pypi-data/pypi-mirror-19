import argparse
import json
import sys

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

    print(json.dumps(
        char2image.chars_to_images(
            [line.strip() for line in args.character_file],
            char2image.filename_to_font(args.font_file, args.size),
            unknown_char=args.unknown_char),
        ensure_ascii=False))


if __name__ == '__main__':
    main()
