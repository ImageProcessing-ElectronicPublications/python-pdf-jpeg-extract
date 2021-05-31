#!/usr/bin/env python

import sys

with open(sys.argv[1],"rb") as file:
    file.seek(0)
    pdf = file.read()

startmark = b"\xff\xd8"
startmark2 = b"\x00\x00\x00\x0C"
startfix = 0
endmark = b"\xff\xd9"
endfix = 2
i = 0

njpg = 0
while True:
    istream = pdf.find(b"stream", i)
    if istream < 0:
        break
    istart = pdf.find(startmark, istream, istream + 20)
    istart2 = pdf.find(startmark2, istream, istream + 20)
    if (istart < 0) and (istart2 < 0):
        i = istream + 20
        continue
    if istart2 < 0:
        iend = pdf.find(b"endstream", istart)
    if istart < 0:
        iend = pdf.find(b"endstream", istart2)
    if iend < 0:
        raise Exception("Didn't find end of stream!")
    iend = pdf.find(endmark, iend - 20)
    if iend < 0:
        raise Exception("Didn't find end of JPG!")

    if istart2 < 0:
        istart += startfix
        iend += endfix
        print("JPG %d from %d to %d" % (njpg, istart, iend))
        jpg = pdf[istart:iend]
        with open("jpg%04d.jpg" % njpg, "wb") as jpgfile:
            jpgfile.write(jpg)
    if istart < 0:
        istart2 += startfix
        iend += endfix
        print("JP2 %d from %d to %d" % (njpg, istart, iend))
        jp2 = pdf[istart2:iend]
        with open("jpg%04d.jp2" % njpg, "wb") as jpxfile:
            jpxfile.write(jp2)

    njpg += 1
    i = iend
