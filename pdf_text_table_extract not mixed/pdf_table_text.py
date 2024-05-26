import pdfplumber
from tabula import read_pdf
import camelot
from tabulate import tabulate
import pandas as pd
def extract_text_and_tables(pdf_path):

  with pdfplumber.open(pdf_path) as pdf:
    text_outside_tables = []
    tables = []

    for page in pdf.pages:            
      all_elements = page.extract_text(x0=0, y0=0, x1=page.width, y1=page.height)
      elements = all_elements.split("\n")

      col2str = {'dtype': str}
      kwargs = {
            'output_format': 'dataframe',
            'pandas_options': col2str,
            'stream': True,           
            'multiple_tables':  True,
            'encoding':'utf-8',
            }

      tables = read_pdf(pdf_path,pages="1",**kwargs)
      print('tables: ',len(tables))
      extracted_tables = pd.concat(tables, ignore_index=True).map(str)

      text_outside_tables = []
      for element in elements:
        found = False
        
        for row in extracted_tables.itertuples(index=False):
            
            fulltext=''
            for cell in row:
               fulltext=fulltext+cell.replace('NaN','').replace('nan','').replace(r'^Unnamed.*$', '')
                        
            if fulltext.replace(' ', '') == element.replace(' ', '') :
                found = True
                print('\n \n *********************matched***************** \n \n')                
                break

        if not found:
            text_outside_tables.append(element.strip())

  return text_outside_tables, tables
  
text_outside_tables, tables = extract_text_and_tables("6.pdf")
for line in text_outside_tables:
  print(line)

print("\nExtracted tables:")
for table in tables:
  print(table)
