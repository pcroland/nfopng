#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from rich import print

parser = argparse.ArgumentParser(
    add_help=False, formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=40)
)
parser.add_argument('-h', '--help',
                    action='help',
                    default=argparse.SUPPRESS,
                    help='shows this help message.')
parser.add_argument('-v', '--version',
                    action='version',
                    version='nfopng 1.0.0',
                    help='shows version.')
parser.add_argument('-i', '--input',
                    help='NFO input file')
parser.add_argument('-o', '--output',
                    help='PNG output file\ndefault: input with .png suffix, or stdout if input is stdin')
parser.add_argument('-min',
                    type=int,
                    default=30,
                    help='minimum brightness\ndefault: 30')
parser.add_argument('-max',
                    type=int,
                    default=200,
                    help='minimum brightness\ndefault: 200')
parser.add_argument('-b', '--border',
                    type=int,
                    default=4,
                    help='border on image\ndefault: 4')
parser.add_argument('-dcb', '--disable-custom-blocks',
                    action='store_true',
                    help='disable custom "░▒▓█▀▄▌▐" characters.')
parser.add_argument('-dcl', '--disable-custom-lines',
                    action='store_true',
                    help='disable custom "■┌┐└┘─│" characters.')
parser.add_argument('-f', '--font',
                    type=str,
                    default='FiraCode',
                    help='font to use\ndefault: FiraCode')
parser.add_argument('-lf', '--list-fonts',
                    action='store_true',
                    help='list fonts')
args = parser.parse_args()


def clamp(inp, low, high):
    return min(max(inp, low), high)


def main():
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    font_list = os.listdir('fonts')
    font_list = [os.path.splitext(font)[0] for font in font_list]

    if args.list_fonts:
        for f in font_list:
            print(f'[green]{f}[/green]')
        sys.exit(0)

    min_bright = clamp(args.min, 0 , 255)
    max_bright = clamp(args.max, 0 , 255)
    c0 = (min_bright, min_bright, min_bright)
    c1 = (int(min_bright + (1 * ((max_bright - min_bright) / 4))), int(min_bright + (1 * ((max_bright - min_bright) / 4))), int(min_bright + (1 * ((max_bright - min_bright) / 4))))
    c2 = (int(min_bright + (2 * ((max_bright - min_bright) / 4))), int(min_bright + (2 * ((max_bright - min_bright) / 4))), int(min_bright + (2 * ((max_bright - min_bright) / 4))))
    c3 = (int(min_bright + (3 * ((max_bright - min_bright) / 4))), int(min_bright + (3 * ((max_bright - min_bright) / 4))), int(min_bright + (3 * ((max_bright - min_bright) / 4))))
    c4 = (max_bright, max_bright, max_bright)

    if args.font not in font_list:
        print(f'[red]ERROR: [bold yellow]{args.font}[/bold yellow] not in font list.[/red]')
        sys.exit(1)

    if args.font == 'FiraCode':
        base_font = ImageFont.truetype(f'fonts/{args.font}.ttf', 13)
    else:
        base_font = ImageFont.truetype(f'fonts/{args.font}.ttf', 16)
    secondary_font = ImageFont.truetype('fonts/FiraCode.ttf', 13)

    chars = '■┌┐└┘─│+-*,@/\.:()[]\'"=_abcdefghijklmnoöpqrstuüvwxyzABCDEFGHIJKLMNOÖPQRSTUÜVWXYZ0123456789░▒▓█▀▄▌▐'
    chars_drw = {}

    for char in chars:
        letter = Image.new('RGB', (8, 16), color = c0)
        drw = ImageDraw.Draw(letter)
        drw.text((0, 0), char, fill=(max_bright, max_bright, max_bright), font=base_font)
        chars_drw[char] = letter

    if not args.disable_custom_blocks:
        shade1 = Image.new('RGB', (8, 16), color = c1)
        shade2 = Image.new('RGB', (8, 16), color = c2)
        shade3 = Image.new('RGB', (8, 16), color = c3)
        shade4 = Image.new('RGB', (8, 16), color = c4)

        vertical_half = Image.new('RGB', (4, 16), color = c4)
        half_left = Image.new('RGB', (8, 16), color = c0)
        half_left.paste(vertical_half, (0, 0))
        half_right = Image.new('RGB', (8, 16), color = c0)
        half_right.paste(vertical_half, (4, 0))

        horizontal_half = Image.new('RGB', (8, 8), color = c4)
        half_upper = Image.new('RGB', (8, 16), color = c0)
        half_upper.paste(horizontal_half, (0, 0))
        half_lower = Image.new('RGB', (8, 16), color = c0)
        half_lower.paste(horizontal_half, (0, 8))
        chars_drw['░'] = shade1
        chars_drw['▒'] = shade2
        chars_drw['▓'] = shade3
        chars_drw['█'] = shade4
        chars_drw['▀'] = half_upper
        chars_drw['▄'] = half_lower
        chars_drw['▌'] = half_left
        chars_drw['▐'] = half_right

    if not args.disable_custom_lines:
        line_h = Image.new('RGB', (8, 2), color = c4)
        line_h_half = Image.new('RGB', (5, 2), color = c4)
        line_v = Image.new('RGB', (2, 16), color = c4)
        line_v_half = Image.new('RGB', (2, 9), color = c4)

        line_horizontal = Image.new('RGB', (8, 16), color = c0)
        line_horizontal.paste(line_h, (0, 7))
        line_vertical = Image.new('RGB', (8, 16), color = c0)
        line_vertical.paste(line_v, (3, 0))

        corner_upper_left = Image.new('RGB', (8, 16), color = c0)
        corner_upper_left.paste(line_v_half, (3, 7))
        corner_upper_left.paste(line_h_half, (3, 7))
        corner_upper_right = Image.new('RGB', (8, 16), color = c0)
        corner_upper_right.paste(line_v_half, (3, 7))
        corner_upper_right.paste(line_h_half, (0, 7))
        corner_lower_left = Image.new('RGB', (8, 16), color = c0)
        corner_lower_left.paste(line_v_half, (3, 0))
        corner_lower_left.paste(line_h_half, (3, 7))
        corner_lower_right = Image.new('RGB', (8, 16), color = c0)
        corner_lower_right.paste(line_v_half, (3, 0))
        corner_lower_right.paste(line_h_half, (0, 7))

        square_a = Image.new('RGB', (6, 6), color = c4)
        square = Image.new('RGB', (8, 16), color = c0)
        square.paste(square_a, (1, 5))

        chars_drw['┌'] = corner_upper_left
        chars_drw['┐'] = corner_upper_right
        chars_drw['└'] = corner_lower_left
        chars_drw['┘'] = corner_lower_right
        chars_drw['─'] = line_horizontal
        chars_drw['│'] = line_vertical
        chars_drw['■'] = square

    if args.input == '-':
        sys.stdin.reconfigure(encoding='cp437')
        nfo = sys.stdin.readlines()
    else:
        with open(args.input, encoding='cp437') as fd:
            nfo = fd.readlines()

    width = (len(max(nfo, key=len)) * 8) + 8
    height = (len(nfo) * 16) + 8

    i = Image.new('RGB', (width, height), color = c0)
    d = ImageDraw.Draw(i)

    y_pos = 4
    for line in nfo:
        x_pos = 4
        for char in line:
            if char == ' ': pass
            elif char in chars: i.paste(chars_drw.get(char), (x_pos, y_pos))
            else: d.text((x_pos, y_pos), char, fill=c4, font=secondary_font)
            x_pos += 8
        y_pos += 16

    if not args.output:
        if args.input == '-':
            args.output = '-'
        else:
            args.output = Path(args.input).with_suffix('.png')

    if args.output == '-':
        if sys.stdout.isatty():
            print('WARNING: Not outputting to stdout because it is a terminal. Please redirect the output to a file.', file=sys.stdout)
            sys.exit(1)
        i.save(sys.stdout, 'png')
    else:
        i.save(args.output)

if __name__ == '__main__':
    main()
