from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar,LTLine,LAParams
import os
# path='ivi.pdf'
# os.chdir(path)
Extract_Data=[]
# for PDF_file in os.listdir():
#     if PDF_file.endswith('.pdf'):
for page_layout in extract_pages('ivi.pdf'):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            for text_line in element:
                for character in text_line:
                    if isinstance(character, LTChar):
                        Font_size=character.size
            Extract_Data.append([Font_size,(element.get_text())])

print(Extract_Data)