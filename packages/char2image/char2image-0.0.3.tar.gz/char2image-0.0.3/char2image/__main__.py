import argparse
import json
import sys

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
        char2image.char_to_image_dict(
            {char for char in args.document_file.read()},
            char2image.filename_to_font(args.font_file, args.size)),
        ensure_ascii=False))


if __name__ == '__main__':
    main()
