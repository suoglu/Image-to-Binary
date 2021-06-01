# Image to Binary

## Contents of Readme

1. About
2. Usage 
3. Raw File
4. Dependencies

[![Repo on GitLab](https://img.shields.io/badge/repo-GitLab-6C488A.svg)](LINK)
[![Repo on GitHub](https://img.shields.io/badge/repo-GitHub-3D76C2.svg)](LINK)

---

## About

Simple script to convert images to BMP files or raw RGB binary file.

## Usage

Script should be called with arguments. First options should be given, if wanted, than the name of the files. Available options can be found at the table below.

| Option | Short version | Description | Default |
| :----: | :----: | :----: | :----:  |
 |`--alpha`|`-a` | Include alpha value in raw file | No |
 |`--bmp`|`-b` | Set output to .bmp | No |
 |`--help`|`-h` | Print usage information | n/a |
 |`--no-alpha`|`-n` | Do not include alpha value in raw file | Yes |
 |`--raw`|`-r` | Set output to .raw | Yes |

## Raw file

Raw files contains binary data values for images, without any header or footer. With `--no-alpha` option, first three bytes holds the RGB values (in that order) for first pixel. Following three bytes hold the values for next pixel and so on. With `--alpha` option, alpha value is included after green value, and each pixel represented with four bytes. 

## Dependencies

Script [image-to-binary.py](Sources/image-to-binary.py) uses sys, os and PIL modules, and tested with Python 3.8.6 on Pop!_OS 20.10
