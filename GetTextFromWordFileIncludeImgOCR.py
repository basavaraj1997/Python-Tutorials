import re
import docx
from io import BytesIO
from PIL import Image
import pytesseract
from os.path import basename
# Set the path to the Tesseract OCR executable (replace with your actual path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_word_document(doc_path):
    doc = docx.Document(doc_path)
    text_content = []    
    pattern = re.compile('rId\d+')
    for graph in doc.paragraphs:
        page_text = ''
        for run in graph.runs:
            if run.text != '':
                page_text+=(run.text)
            else:                
                contentID = pattern.search(run.element.xml).group(0)
                try:
                    contentType = doc.part.related_parts[contentID].content_type
                except KeyError as e:
                    print(e)
                    continue
                if not contentType.startswith('image'):
                    continue
                imgName = basename(doc.part.related_parts[contentID].partname)
                imgData = doc.part.related_parts[contentID].blob
                image_stream = BytesIO(imgData)
                img = Image.open(image_stream)
                img_text = pytesseract.image_to_string(img)
                page_text+=img_text
          
        text_content.append(page_text)

    return text_content

if __name__ == "__main__":
    document_path = "your_word_filename.docx"
    extracted_text = extract_text_from_word_document(document_path)

    for i, text in enumerate(extracted_text, start=1):
        print(f"{text}\n")
