#!/usr/bin/env python

import sys
import argparse

PROGNAME = 'pdf-jpeg-extract-dirty.py'
VERSION = '0.2'

def pdf_extract_images(pdfname, prefix):
    startmarkjpg = b"\xff\xd8"
    startmarkjp2 = b"\x00\x00\x00\x0C"
    startfix = 0
    endmarkjp = b"\xff\xd9"
    endfix = 2
    i = 0

    with open(pdfname) as file:
        file.seek(0)
        pdf = file.read()

    njpg = 0
    while True:
        istream = pdf.find(b"stream", i)
        if istream < 0:
            break
        iend = pdf.find(b"endstream", istream)
        if iend < 0:
            break
        iformat = ""
        istartjpg = pdf.find(startmarkjpg, istream, istream + 20)
        istartjp2 = pdf.find(startmarkjp2, istream, istream + 20)
        if ((istartjpg >= 0) or (istartjp2 >= 0)):
            istart = 0
            if (istartjpg >= istartjp2):
                iformat = "jpg"
                istart = istartjpg
            else:
                iformat = "jp2"
                istart = istartjp2
            iend = pdf.find(endmarkjp, iend - 20)
            if (iend < 0):
                raise Exception("Didn't find end of JPG!")

            istart += startfix
            iend += endfix
            print("%s %d from %d to %d" % (iformat, njpg, istart, iend))
            jp = pdf[istart:iend]
            with open(prefix + "%04d." % njpg + iformat, "wb") as jpfile:
                jpfile.write(jp)
            njpg += 1
            i = iend
        else:
            i = istream + 20

def print_version():
    print (PROGNAME)
    print (VERSION)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract JPEG and JP2 from PDF')
    parser.add_argument(
        '-p',
        '--prefix',
        metavar='prefix',
        type=str,
        default='img',
        help='prefix output image name, default img')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=print_version())
    parser.add_argument('pdfname', help='PDF file name')
    args = parser.parse_args()
    pdf_extract_images(args.pdfname, args.prefix)
