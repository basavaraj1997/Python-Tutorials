import json
import pdfplumber

def extract_table_text(normal_text_coords, table_text_coords,table_text):
    # Define the bounding box for the normal text
    normal_text_bbox = (normal_text_coords['x0'], normal_text_coords['top'],
                        normal_text_coords['x1'], normal_text_coords['bottom'])

    # Define the bounding box for the table text
    table_text_bbox = (table_text_coords[0], table_text_coords[1],
                       table_text_coords[2], table_text_coords[3])

    is_outside = ( normal_text_bbox[2] < table_text_bbox[0] or
                    normal_text_bbox[0] > table_text_bbox[2] or
                    normal_text_bbox[3] < table_text_bbox[1] or
                    normal_text_bbox[1] > table_text_bbox[3])
      
    return is_outside
 
def extract_text_and_tables(pdf_path):

  with pdfplumber.open(pdf_path) as pdf:
    text_inSequence=[]

    for page in pdf.pages:
      text_inSequence.append('\n \n **************'+str(page.page_number)+'*********** \n \n')
               
      all_elements = page.extract_text_lines(x0=0, y0=0, x1=page.width, y1=page.height)
      elements = all_elements
      tbls_location=page.find_tables()
      tbls=page.extract_tables()      
      

      for element in elements:
        if len(tbls_location) == 0:
           text_inSequence.append(element['text'])
           continue
        i=0
        for table in tbls_location:             
            is_outside=extract_table_text(element, table.bbox,'')
            if is_outside:
               text_inSequence.append(element['text'])
               break
            i=i+1
      text_inSequence.append(json.dumps(tbls))
  return text_inSequence
file_path="6.pdf"
text_inSequence = extract_text_and_tables(file_path)

print("\nExtracted Text, tables:")
for text_table in text_inSequence:
  print(text_table)
 
with open(file_path.split('.')[0]+'tbltxt_.txt', 'w',encoding="utf-8") as file:
   for text_table in text_inSequence:
      file.write(str(text_table)+'\n')