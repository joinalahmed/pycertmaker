#!/usr/bin/env python
"""
Simple Python script that combines a folder of pdfs into a single
pdf. By default the pdfs are merged in alphabetical order and 
only appear once. To change this create a "list.txt" file in the 
directory with the pdfs to merge and list the order of the pdfs 
to merge.

Ex list.txt:
doc2.pdf
doc1.pdf
doc2.pdf

To use the script:
python PDFMerge.py /path/to/pdf/dir output.pdf
"""

import os
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader  
    
def main():
    
    # Saving arguments
    pdfDir = sys.argv[1]
    if(sys.argv[2].endswith(".pdf") == False):
        filename = sys.argv[2] + ".pdf"
    else:
        filename = sys.argv[2]
    print "Directory to merge: %s" % pdfDir
    print "File to create: %s" % filename
    
    # Check if path exists, then change directory
    if(os.path.exists(pdfDir) == True):
        print "Changing to directory"
        os.chdir(pdfDir)
        if(os.path.isfile(filename) == True):
            os.remove(filename)
    else:
        print "Path doesn't exist"
        sys.exit()
        
    # Check if list.txt exists
    if(os.path.isfile("list.txt") == True):
        print "Found list.txt"
        order = True
    else:
        print "No list.txt, doing in alphabetical order"
        order = False
    
    # Getting list of files
    files = []
    if(order == True):
        f = open('list.txt', 'r')
        for line in f:
            line = line.strip()
            if((line.endswith(".pdf") == True) and (os.path.isfile(line) == True)):
                files.append(line)
    else:
        dirFiles = os.listdir('.')
        dirFiles.sort()
        for foundFile in dirFiles:
            if(foundFile.endswith(".pdf") == True):
                files.append(foundFile)
    if(len(files) < 1):
        print "No files found for merging"
        sys.exit()
        
    # Doing the pdf merge
    pdfOutput = PdfFileWriter()
    for pdfFile in files:
        print "Adding %s" % pdfFile
        pdfInput = PdfFileReader(open(pdfFile, "rb"))
        numPages = pdfInput.getNumPages()
        for i in range(numPages):
            pdfOutput.addPage(pdfInput.getPage(i))
    outputStream = file(filename, "wb")
    pdfOutput.write(outputStream)
    
    
if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print "Incorrect number of parameters."
        print "Usage: python PDFMerge.py path/to/pdf/dir output.pdf"
        sys.exit()
    main()
