#!/usr/bin/env python3
# coding=utf-8
import argparse
import json
import os
from string import Template
from colorama import Fore, Style
from pygments import highlight, formatters, lexers

banner = '''
         __    ___        __    _
  ___ _ / /_  / _/ ___   / /   (_)  ___   ___
 / _ `// __/ / _/ / _ \ / _ \ / /  / _ \ (_-<
 \_, / \__/ /_/   \___//_.__//_/  /_//_//___/
/___/
'''

data_dir = "data/"
json_ext = ".json"

info = Template(Style.BRIGHT + '[ ' + Fore.GREEN + '*' + Fore.RESET + ' ] ' + Style.RESET_ALL + '$text')
fail = Template(Style.BRIGHT + '[ ' + Fore.RED + '-' + Fore.RESET + ' ] ' + Style.RESET_ALL + '$text')
title = Template(
    '\n' + Style.BRIGHT + '---------- [ ' + Fore.CYAN + '$title' + Fore.RESET + ' ] ----------' + Style.RESET_ALL + '\n'
)
description = Template(Style.DIM + '# ' + '$description' + Style.RESET_ALL)
divider = '\n' + Style.BRIGHT + ' - ' * 10 + Style.RESET_ALL + '\n'
sep =  '\n' + Style.BRIGHT + '-' * 100 + Style.RESET_ALL + '\n'  



def parse_args():
    parser = argparse.ArgumentParser(usage="python3 gtfo.py [binary]",
                                     description="Command-line program for GTFOBins. "
                                                 "It helps you to bypass system security restrictions. Version 1.0")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-b', '--binary', action='store', help='specifies the binary file')
    parser.add_argument('-l', '--list')
    return parser.parse_args()



def main(binary):
    print(Fore.YELLOW + sep  + " " * 45 + binary.upper() + Fore.YELLOW + sep + Style.RESET_ALL,end='')
    file_path = data_dir + binary + json_ext
    if os.path.isfile(file_path):
        with open(file_path) as source:
            data = source.read()

        json_data = json.loads(data)
        if 'description' in json_data:
            print('\n' + description.safe_substitute(description=json_data['description']),end='')

        for vector in json_data['functions']:
            print(title.safe_substitute(title=str(vector).upper()),end='')
            index = 0
            for code in json_data['functions'][vector]:
                index = index + 1
                if 'description' in code:
                    print(description.safe_substitute(description=code['description']),end='' + '\n')
                print(highlight(code['code'], lexers.BashLexer(),
                                formatters.TerminalTrueColorFormatter(style='igor')).strip())
                if index != len(json_data['functions'][vector]):
                    print(divider,end='')
    else:
        print(fail.safe_substitute(text="Sorry, couldn't find anything for " + binary),end='')


def list():
    file = open('list.txt', 'r')
    Lines = file.readlines()
    count = 0

    for line in Lines:
        count += 1
        main(line.strip())

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    args = parse_args()
    if args.list:
        list() 
    else:
        main(binary=args.binary)
