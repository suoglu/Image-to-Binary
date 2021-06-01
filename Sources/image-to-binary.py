#!/usr/bin/env python3

#*-------------------------------------------*#
#  Title       : Image to Binary Converter    #
#  File        : image-to-binary.py           #
#  Author      : Yigit Suoglu                 #
#  License     : EUPL-1.2                     #
#  Last Edit   : 01/06/2021                   #
#*-------------------------------------------*#
#  Description : Python3 script to convert    #
#                image files to binary        #
#                bitmaps                      #
#*-------------------------------------------*#

import sys
import os

from PIL import Image


#Helper functions for printing, coloring
def print_error(msg): sys.stdout.write('\033[31m' + msg + '\033[0m')


def print_success(msg): sys.stdout.write('\033[32m' + msg + '\033[0m')


def print_info(msg): sys.stdout.write('\033[2m' + msg + '\033[0m')


def print_warn(msg): sys.stdout.write('\033[91m' + msg + '\033[0m')


def print_raw(msg):  sys.stdout.write(msg)


def print_help():
    print(' Usage: image-to-binary [-opt] file0, file1, ...')
    print('\n  Available options:')
    print('    -a or --alpha    : include alpha value in raw file')
    print('    -b or --bmp      : generate a .bmp file')
    print('    -h or --help     : print this message')
    print('    -n or --no-alpha : do not include alpha value in raw file')
    print('    -r or --raw      : generate a raw binary file which only contains pixel values')
    print('\n  Default options: --raw --no-alpha')


#Main function
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_warn('Nothing to do!\n')
    else:
        no_alpha = True
        raw = True
        greyscale = False
        while len(sys.argv) > 1:
            arg = sys.argv.pop(1)
            if arg.startswith('-'):
                if arg == '-a' or arg == '--alpha':
                    no_alpha = False
                elif arg == '-n' or arg == '--no-alpha':
                    no_alpha = True
                elif arg == '-b' or arg == '--bmp':
                    raw = False
                elif arg == '-r' or arg == '--raw':
                    raw = True
                elif arg == '-h' or arg == '--help':
                    print_help()
                    sys.exit(0)
                else:
                    print_warn('Unknown command: ')
                    print_raw(arg + '\n')
            else:
                filename = arg
                try:
                    img = Image.open(filename)
                except Exception as err:
                    print_error('Error on \033[0m' + filename + '\033[31m: ' + str(err) + '\n')
                    print_info('Ignoring file...\n')
                    continue
                filename = filename[:filename.rindex('.')]  #remove extension
                file_num = ''
                try:
                    if os.path.isfile(filename + '.bmp'):
                        file_num = 0
                        while os.path.isfile(filename + '_' + str(file_num) + '.bmp'):
                            file_num += 1
                        file_num = '_' + str(file_num)
                    img.save(filename + file_num + '.bmp')
                    img.close()
                    if not raw:
                        print_success('BMP file \033[0m' + filename + file_num + '.bmp' + '\033[32m is generated.\n')
                except Exception as err:
                    print_error('Error when creating ' + filename + file_num + '.bmp: ' + str(err) + '\n')
                    continue
                if raw:
                    bmp_file_name = filename + file_num + '.bmp'
                    try:
                        img_bmp = open(bmp_file_name, 'rb')
                    except Exception as err:
                        print_error('Error when opening ' + bmp_file_name + ': ' + str(err) + '\n')
                        continue
                    try:
                        file_num = ''
                        if os.path.isfile(filename + '.raw'):
                            file_num = 0
                            while os.path.isfile(filename + '_' + str(file_num) + '.raw'):
                                file_num += 1
                            file_num = '_' + str(file_num)
                        raw_file_name = filename + file_num + '.raw'
                        img_raw = open(raw_file_name, 'xb')
                    except Exception as err:
                        print_error('Error when creating ' + filename + file_num + '.raw: ' + str(err) + '\n')
                        continue
                    img_bmp.read(10)  #discard first part of header
                    array_offset = img_bmp.read(1)  #get offset for binary image data
                    byte = img_bmp.read(int.from_bytes(array_offset, byteorder='little')-11)  #discard remaining header
                    byte_counter = 0
                    while byte != b'':
                        byte = img_bmp.read(1)
                        if no_alpha and byte_counter == 3:
                            byte_counter = 0
                        else:
                            img_raw.write(byte)
                            byte_counter += 1
                    img_bmp.close()
                    img_raw.close()
                    if os.path.isfile(bmp_file_name):
                        os.remove(bmp_file_name)
                    print_success('Binary image file \033[0m' + raw_file_name + '\033[32m is generated.\n')
    sys.exit(0)
