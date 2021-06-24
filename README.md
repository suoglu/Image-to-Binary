# Image to Binary

## Contents of Readme

1. About
2. Usage
4. Input image
5. Raw File
6. Dependencies

[![Repo on GitLab](https://img.shields.io/badge/repo-GitLab-6C488A.svg)](https://gitlab.com/suoglu/image-to-binary)
[![Repo on GitHub](https://img.shields.io/badge/repo-GitHub-3D76C2.svg)](https://github.com/suoglu/Image-to-Binary)

---

## About

Simple script to convert images to BMP files or raw RGB binary file.

## Usage

Script should be called with arguments. First options should be given, if wanted, than the name of the files. Available options can be found at the table below.

| Option | Short version | Description | Default |
| :----: | :----: | :----: | :----:  |
 |`--alpha`|`-a` | Include alpha channel in raw file | No |
 |`--bmp`|`-b` | Set output to .bmp | No |
 |`--help`|`-h` | Print usage information | n/a |
 |`--no-alpha`|`-n` | Do not include alpha channel in raw file | Yes |
 |`--raw`|`-r` | Set output to .raw | Yes |
 |`--format [x]`|`-f [x]` | Manipulates the output image data | No |

Table of available formats for `--format` (`-f`) option:

| Name | Description | Usage information |
| :----: | :----: | :----: |
|`bw`|Black & white output image|Uses input raw/bmp and alpha configuration|
|`greyscale`|Greyscale output image|Uses input raw/bmp and alpha configuration|
|`rgb565`|RGB565 formatted output image|Output is raw data without alpha channel|

## Input Image

This tool should work with any image file that PIL module can open. While doing any of the "formatting" with `--format` or writing a *.raw* file; it uses *.bmp* files with 8-bit colors, with or without alpha channel.

## Raw file

Raw files contains binary data values for images, without any header or footer. With `--no-alpha` option, first three bytes holds the RGB values for first pixel. Following three bytes hold the values for next pixel and so on. With `--alpha` option, alpha value is included after last color value, and each pixel represented with four bytes. RGB values are stored in little byte order, same as BMP file.

## RGB565 format

In standard raw file, each color represented with 8 bits. In RGB565 format; red and blue are represented with 5 bits each, while green is represented with 6 bits. To fit existing 24 bit color data to 16 bits, corresponding color bits are shifted. RGB565 values are stored in big byte order.

## Dependencies

Script [image-to-binary.py](Sources/image-to-binary.py) uses sys, os and PIL modules, and tested with Python 3.8.6 on Pop!_OS 20.10
