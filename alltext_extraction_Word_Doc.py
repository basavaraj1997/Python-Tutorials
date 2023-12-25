
import io
from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
import xml.etree.ElementTree as ET
from PIL import Image
import pytesseract
import re

def get_all_doc_text(file): 
	# file path or file stream data
	document = Document(file)
	word_doc_all_Text = ""
	print(document.add_page_break() )
	for docPart in iter_All_block(document):		
		if isinstance(docPart, Paragraph):
			#Get Document Paragraph text
			for run in docPart.runs:
				if 'lastRenderedPageBreak' in run._element.xml:
					print ('soft page break found at run:'+ run.text[:20])
				if 'w:br' in run._element.xml and 'type="page"' in run._element.xml:
					print ('hard page break found at run:'+ run.text[:20])				
			if re.match("List\sParagraph",docPart.style.name):
				word_doc_all_Text+=docPart.text+"\n"
			else:
				#Get text from image using OCR
				images_text = get_imageText(document,docPart)				
				if len(images_text) > 0:
					word_doc_all_Text = word_doc_all_Text + images_text+"\n"
				word_doc_all_Text = word_doc_all_Text + docPart.text+"\n"
		#Extract Table and convert table in html format 		
		elif isinstance(docPart, Table):
			word_doc_all_Text += convert_html_table(docPart,document)+"\n"    
	return word_doc_all_Text
   
def iter_All_block(parent):
    """
    Generate a reference from each paragraph and table child within parent of document in sequence order.    
    """
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)
		
# Modified to treat cell content as a set of blocks to process 
def convert_html_table(table,document):	
	html_table = "<table>"
	for row in table.rows:
		html_table += "<tr>"
		for cell in row.cells:
			html_table += "<td>"
			# --- 
			cbody = ""
			col_list_data = []
			for cblock in iter_All_block(cell):
				if isinstance(cblock, Paragraph):
					col_list_data.append(cblock.text)
					if re.match("List\sParagraph",cblock.style.name):
						col_list_data.append(table.text )
					else:
						images = get_imageText(document,cblock)
						if len(col_list_data) > 0:
							cbody += " ".join(col_list_data)							
						if len(images) > 0:
							cbody = cbody + images
						else:
							cbody = cbody + cblock.text
				elif isinstance(cblock, Table):
					cbody += convert_html_table(cblock)
			html_table += cbody + " "
			html_table += "</td>"
		html_table += "</tr>"
	html_table += "</table>"
	return html_table

def get_imageText(document,par):
    """Get all images from paragraph
    """
    img_ids = []
    root = ET.fromstring(par._p.xml)
    tag_namespaces = {
             'a':"http://schemas.openxmlformats.org/drawingml/2006/main", \
             'r':"http://schemas.openxmlformats.org/officeDocument/2006/relationships", \
             'wp':"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"}
    imageParentParts = root.findall('.//wp:inline',tag_namespaces)
    for inline in imageParentParts:
        images = inline.findall('.//a:blip', tag_namespaces)
        for img in images:     
            id = img.attrib['{{{0}}}embed'.format(tag_namespaces['r'])]
            img_ids.append(id)
    imageParentParts = root.findall('.//wp:anchor',tag_namespaces)
    for inline in imageParentParts:
        images2 = inline.findall('.//a:blip', tag_namespaces)
        for img2 in images2:     
            id = img2.attrib['{{{0}}}embed'.format(tag_namespaces['r'])]
            img_ids.append(id)
    response = ""
    if len(img_ids) > 0:
        for id in img_ids:
            image_part = document.part.related_parts[id]
            image_stream = io.BytesIO(image_part._blob) 
            img = Image.open(image_stream)
            format = img.format.lower()
            if (format in ("jpeg" ,"png" ,"gif" ,"bmp" ,"tiff" ,"jpg")):
                  img_text = pytesseract.image_to_string(img)
                  response +=img_text
    return response

if __name__ == '__main__':
	s = get_all_doc_text('DataWare1.docx')
	#print(s)
