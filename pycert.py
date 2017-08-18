import csv, os
import PyPDF2
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, letter, landscape
from reportlab.lib.colors import orange, black, red
filepath = os.path.abspath('data/nameslist.csv')



class CertificateMaker():
    def write_string_to_pdf(self, participants_name,workshop_name,workshop_date,workshop_venue):
	participants_nameS =participants_name
        outputfiletemp = 'output/testoutput.pdf'
        pdf1File = open('templates/certificate.pdf', 'rb')
        pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
        pdfWriter = PyPDF2.PdfFileWriter()

        packet = StringIO.StringIO()

        cv=canvas.Canvas(packet, pagesize=letter)
	
        cv.setPageSize(landscape(letter))
	width=letter
        #create a string
	cv.setFont("Courier-BoldOblique", 20)
        cv.drawCentredString(3*(1056/8),360,'This is to Certify that',)
	cv.setFont("Helvetica-Bold", 30)
	cv.setFillColor(red)
        cv.drawCentredString(3*(1056/8), 310, participants_nameS,)
	cv.setFillColor(black)
	cv.setFont("Courier-BoldOblique", 20)
        cv.drawCentredString(3*(1056/8),270,'has attended and successfully completed the',)
	cv.setFont("Helvetica-Bold", 25)
        cv.drawCentredString(3*(1056/8),220,workshop_name,)
	cv.setFont("Courier-BoldOblique", 20)
        cv.drawCentredString(3*(1056/8), 180, 'held on '+workshop_date,)
	
        cv.drawCentredString(3*(1056/8), 150, ' at '+workshop_venue,)
        #save to string
        cv.save()
        #write to a file
        with open(outputfiletemp,'wb') as fp:
            fp.write(packet.getvalue())

        certFirstPage = pdf1Reader.getPage(0)
        pdfWatermarkReader = PyPDF2.PdfFileReader(open(outputfiletemp, 'rb'))
        certFirstPage.mergePage(pdfWatermarkReader.getPage(0))
        pdfWriter.addPage(certFirstPage)

        pdfOutputFile = open('output/certificate_' + participants_name + '.pdf', 'wb')
        pdfWriter.write(pdfOutputFile)
        pdfOutputFile.close()
        pdf1File.close()
	os.remove('output/testoutput.pdf')

if __name__ == "__main__":
    # iterate trough list of names from CSV
    with open(filepath, 'rb') as csvfile:
	
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	count = 0
        for row in spamreader:
	    if count == 0:
		name=row[0]
		count += 1
		continue
	    if count == 1:
		date=row[0]
		count += 1
		continue
	    if count == 2:
		venue=row[0]
		count += 1
		continue
	    if count >= 3:
            	cert = CertificateMaker()
            	cert.write_string_to_pdf(row[0],name,date,venue)
		count += 1

