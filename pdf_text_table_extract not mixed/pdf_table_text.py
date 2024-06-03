import json
import pdfplumber
from tabula import read_pdf
import camelot
from tabulate import tabulate
import pandas as pd
def extract_text_and_tables(pdf_path):

  with pdfplumber.open(pdf_path) as pdf:
    text_outside_tables1 = []
    tables = []
    text_inSequence=[]

    for page in pdf.pages:
      text_inSequence.append('**************'+str(page.page_number)+'*********** \n \n')
      text_outside_tables = []            
      all_elements = page.extract_text(x0=0, y0=0, x1=page.width, y1=page.height)
      elements = all_elements.split("\n")      

      col2str = {'dtype': str}
      kwargs = {
            'output_format': 'dataframe',
            'pandas_options': col2str,
            'guess': True,                       
            'encoding':'utf-8',
            'force_subprocess':False,
            'relative_area':False
            }

      tables = read_pdf(pdf_path,pages=page.page_number,multiple_tables=True,**kwargs)
      print('tables: ',len(tables))
      extracted_tables = [] if len(tables) == 0 else pd.concat(tables, ignore_index=True).map(str)

      text_outside_tables = []
      is_last_row=False
      for element in elements:
        found = False

        if is_last_row or len(tables) == 0:
           text_inSequence.append(element.strip())
           continue
           
        i=0
        for row in extracted_tables.itertuples(index=False):
            i=i+1 
            fulltext=''
            for cell in row:
               cell=cell.replace('NaN','').replace('nan','')
               fulltext=fulltext+cell.replace('NaN','').replace('nan','').replace(r'^Unnamed.*$', '')
                        
            if fulltext.replace(' ', '') == element.replace(' ', '') :
                found = True
                print('\n \n *********************matched***************** \n \n') 
                if (len(extracted_tables.values))==i:
                   is_last_row=True
                break
        if is_last_row:
           for line in text_outside_tables:
              text_inSequence.append(line)
           text_inSequence.append(json.dumps(json.loads(extracted_tables.to_json(orient="records"))))
        if not found:
            text_outside_tables.append(element.strip())
            text_outside_tables1.append(element.strip())

            
  return text_inSequence
file_path="15.pdf"
text_inSequence = extract_text_and_tables(file_path)

print("\nExtracted Text, tables:")
for text_table in text_inSequence:
  print(text_table)
 
with open(file_path.split('.')[0]+'.txt', 'w') as file:
   for text_table in text_inSequence:
      file.write(text_table)
