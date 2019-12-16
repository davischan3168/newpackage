#!/usr/bin/env python3
# -*-coding:utf-8-*-

from PyPDF2 import PdfFileWriter, PdfFileReader
import sys
import os
def pdfcrop(inf,outf=None,\
            left_margin=80,low_margin=75,\
            right_margin=80,up_margin=40):
    """
    (left_margin,low_margin): 取左下角，该点为页面的左下点为原点，
                              left_margin:为横轴上的点
                              low_margin: 为纵轴上的点
    (right_margin,up_margin): 取右上点，该点为页面的右上点为原点，
                              right_margin:为横轴上的点
                              up_margin:   为纵轴上的点
    """
    input1 = PdfFileReader(inf,'rb')
    output = PdfFileWriter()
    numPages = input1.getNumPages()
    print("document has %s pages." % numPages)
    for i in range(numPages):
        page = input1.getPage(i)
        print(page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y())
        #page.trimBox.lowerLeft = (25, 25)
        #page.trimBox.upperRight = (225, 225)
        page.cropBox.lowerLeft = (left_margin,low_margin)
        page.cropBox.upperRight = (page.mediaBox.getUpperRight_x()-right_margin,page.mediaBox.getUpperRight_y()-up_margin)
        output.addPage(page)
    if (outf=='') or (outf is None):
        outf=os.path.splitext(inf)[0]+'_crop.pdf'
    outputStream = open(outf, "wb")
    output.write(outputStream)
    outputStream.close()
    return

if __name__=="__main__":
    pdfcrop(sys.argv[1])
    pass
