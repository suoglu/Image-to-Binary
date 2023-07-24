#!/usr/bin/env python3

#*-------------------------------------------*#
#  Title       : Image to Binary Converter    #
#  File        : image-to-binary.py           #
#  Author      : Yigit Suoglu                 #   
#  License     : EUPL-1.2                     #
#  Last Edit   : 24/07/2023                   #
#*-------------------------------------------*#
#  Description : Python3 script to convert    #
#                image files to binary        #
#                bitmaps                      #
#*-------------------------------------------*#

import sys
import os

from PIL import Image


class UnknownFormat(TypeError):
  pass


def calculate565rgb(r: int, g: int, b: int) -> int:
  red_scaled = r >> 3
  green_scaled = g >> 2
  blue_scaled = b >> 3
  result_2bytes = blue_scaled | (green_scaled << 5) | (red_scaled << 11)
  return result_2bytes


def calculate_grey(r: int, g: int, b: int) -> int:
  grey = 0.299 * float(r) + 0.587 * float(g) + 0.114 * float(b)
  return int(round(grey))


def calculate_bw(grey: int) -> int:
  if grey > 127:  #white
    return 255
  else:  #black
    return 0


#Helper functions for printing, coloring
def print_error(msg): sys.stdout.write('\033[31m' + msg + '\033[0m')


def print_success(msg): sys.stdout.write('\033[32m' + msg + '\033[0m')


def print_info(msg): sys.stdout.write('\033[2m' + msg + '\033[0m')


def print_warn(msg): sys.stdout.write('\033[91m' + msg + '\033[0m')


def print_raw(msg):  sys.stdout.write(msg)


def print_help():
  print(' Usage: image-to-binary [-opt] file0, file1, ...')
  print('\n  Available options:')
  print('  -a or --alpha      : include alpha value in raw file')
  print('  -b or --bmp        : generate a .bmp file')
  print('  -h or --help       : print this message')
  print('  -n or --no-alpha   : do not include alpha value in raw file')
  print('  -r or --raw        : generate a raw binary file which only contains pixel values')
  print('  -f or --format [x] : specify output format')
  print('\n   Default options: --raw --no-alpha')
  print('\n  Available Formats:')
  print('        rgb565       : RGB format with 5 bit red, 6 bit green and 5 bit blue; output is always raw')
  print('        greyscale    : Greyscale image, bmp or 8 bit raw')
  print('        bw           : Black and white image, bmp or 1 bit raw ')


#Main function
if __name__ == '__main__':
  if len(sys.argv) == 1:  #Always need arguments
    print_warn('Nothing to do!\n')
    sys.exit(0)

  files = []
  no_alpha = True
  raw = True
  greyscale = False
  mode_rgb565 = False
  mode_bw = False
  mode_grey = False
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
      elif arg == '-f' or arg == '--format':
        try:
          arg = sys.argv.pop(1)
        except IndexError:
          print_error('Format information missing\n')
          sys.exit(1)
        except Exception as err:
          print_error('Error: ' + str(err) + '\n')
          sys.exit(1)
        if mode_bw or mode_grey or mode_rgb565:
          print_warn('Multiple formats given!\n')
          print_info('Ignoring \033[0m' + arg + '\n')
          continue
        arg = arg.casefold()
        if arg == 'rgb565':
          mode_rgb565 = True
        elif arg == 'bw' or arg.startswith('black'):
          mode_bw = True
        elif arg.startswith('grey'):
          mode_grey = True
        else:
          print_warn('Unknown format: ')
          print_raw(arg + '\n')
      else:
        print_warn('Unknown command: ')
        print_raw(arg + '\n')
        sys.exit(1)
    else:
      files.append(arg)
  for filename in files:
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
      if not raw and not mode_bw and not mode_grey and not mode_rgb565:
        print_success('BMP file \033[0m' + filename + file_num + '.bmp' + '\033[32m is generated.\n')
    except Exception as err:
      print_error('Error when creating ' + filename + file_num + '.bmp: ' + str(err) + '\n')
      sys.exit(1)
    if mode_bw or mode_grey or mode_rgb565 or raw:
      bmp_file_name = filename + file_num + '.bmp'
      try:
        img_bmp = open(bmp_file_name, 'rb')
      except Exception as err:
        print_error('Error when opening ' + bmp_file_name + ': ' + str(err) + '\n')
        sys.exit(1)
      if mode_bw or mode_grey:
        # determine output filename
        if mode_bw:
          mode_name = '.bw'
        else:
          mode_name = '.grey'
        if raw:
          f_ext = '.raw'
        else:
          f_ext = '.bmp'
        #create that file
        try:
          file_num = ''
          if os.path.isfile(filename + mode_name + f_ext):
            file_num = 0
            while os.path.isfile(filename + mode_name + '_' + str(file_num) + f_ext):
              file_num += 1
            file_num = '_' + str(file_num)
          out_file_name = filename + mode_name + file_num + f_ext
          img_out = open(out_file_name, 'xb')
        except Exception as err:
          print_error('Error when creating ' + filename + file_num + f_ext + ': ' + str(err) + '\n')
          continue
        try:
          if not raw:  #write bmp header, same as original
            img_out.write(img_bmp.read(10))
          else:
            img_bmp.read(10)
          array_offset = img_bmp.read(4)  #get offset for binary image data
          if not raw:
            img_out.write(array_offset)
            img_out.write(img_bmp.read(14))
          else:
            img_bmp.read(14)
          pix_size = img_bmp.read(2)
          if not raw:
            img_out.write(pix_size)
          pix_size = int.from_bytes(pix_size, byteorder='little')  #get pixel size
          if pix_size == 24:
            contains_alpha = False
          elif pix_size == 32:
            contains_alpha = True
            print('alpha')
          else:
            print_info('Pixel size: ' + str(pix_size) + '\n')
            raise UnknownFormat
          header_remain = int.from_bytes(array_offset, byteorder='little') - 21
          byte = img_bmp.read(header_remain)  #remaining of the header
          if not raw:
            img_out.write(byte)
          byte = img_bmp.read(1)
          while byte != b'':
            try:
              alpha = b''
              blue = int.from_bytes(byte, byteorder='little')
              green = int.from_bytes(img_bmp.read(1), byteorder='little')
              red = int.from_bytes(img_bmp.read(1), byteorder='little')
              if contains_alpha:
                alpha = img_bmp.read(1)
              calc_pixel = calculate_grey(red, green, blue)
              if mode_bw:
                calc_pixel = calculate_bw(calc_pixel)
              byte = calc_pixel.to_bytes(1, byteorder='little')
              for i in range(3):
                img_out.write(byte)
              if contains_alpha:
                img_out.write(alpha)
              byte = img_bmp.read(1)
            except Exception as err:
              print_error('Something went wrong: ' + str(err) + '\n')
              break
          if mode_grey:
            colour_str = 'Greyscale'
          else:
            colour_str = 'Black & white'
          if raw:
            type_str = 'binary image'
          else:
            type_str = 'BMP'
          print_success(colour_str + ' ' + type_str + ' file \033[0m' + out_file_name + '\033[32m is generated.\n')
          img_out.close()
        except UnknownFormat:
          print_error('Unknown image format!\n')
          img_bmp.close()
          img_out.close()
          sys.exit(1)
        except Exception as err:
          print_error('Cannot write bmp file: ' + str(err) + '\n')
          sys.exit(1)
      elif raw or mode_rgb565:
        mode_name = ''
        try:
          file_num = ''
          if mode_rgb565:
            mode_name = '.rgb565'
          if os.path.isfile(filename + mode_name + '.raw'):
            file_num = 0
            while os.path.isfile(filename + mode_name + '_' + str(file_num) + '.raw'):
              file_num += 1
            file_num = '_' + str(file_num)
          out_file_name = filename + mode_name + file_num + '.raw'
          img_out = open(out_file_name, 'xb')
        except Exception as err:
          print_error('Error when creating ' + filename + mode_name + file_num + '.raw: ' + str(err) + '\n')
          continue
        try:
          img_bmp.read(10)  #discard first part of header
          array_offset = img_bmp.read(4)  #get offset for binary image data
          byte = img_bmp.read(14)  #discard remaining of header
          pix_size = int.from_bytes(img_bmp.read(2), byteorder='little')  #get pixel size
          if pix_size == 24:
            contains_alpha = False
          elif pix_size == 32:
            contains_alpha = True
          else:
            raise UnknownFormat
          img_bmp.close()
          try:
            img_bmp = open(bmp_file_name, 'rb')
          except Exception as err:
            print_error('Error when reopening ' + bmp_file_name + ': ' + str(err) + '\n')
            sys.exit(1)
          byte_counter = 0
          img_bmp.read(int.from_bytes(array_offset, byteorder='little'))  #discard header
          byte = img_bmp.read(1)
          if mode_rgb565:
            while byte != b'':
              blue = int.from_bytes(byte, byteorder='little')
              green = int.from_bytes(img_bmp.read(1), byteorder='little')
              red = int.from_bytes(img_bmp.read(1), byteorder='little')
              if contains_alpha:
                img_bmp.read(1)
              rgb = calculate565rgb(red, green, blue)
              img_out.write(rgb.to_bytes(2, byteorder='big'))
              byte = img_bmp.read(1)
            print_success('Binary RGB565 image file \033[0m' + out_file_name + '\033[32m is generated.\n')
            print_info('Byte order is big\n')
          else:
            while byte != b'':
              if no_alpha and contains_alpha and byte_counter == 3:
                byte_counter = 0
              else:
                img_out.write(byte)
                byte_counter += 1
              byte = img_bmp.read(1)
            print_success('Binary image file \033[0m' + out_file_name + '\033[32m is generated.\n')
            print_info('Byte order is little\n')
          img_out.close()
        except UnknownFormat:
          print_error('Unknown image format!\n')
          img_bmp.close()
          img_out.close()
          continue
        except Exception as err:
          print_error('Error: ' + str(err) + '\n')
          sys.exit(1)
      img_bmp.close()
      if os.path.isfile(bmp_file_name):
        os.remove(bmp_file_name)
  sys.exit(0)
