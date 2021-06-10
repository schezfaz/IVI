import pdfplumber
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LAParams


def extract_character_characteristics(pdf_file):
    number_of_pages = len(list(extract_pages(pdf_file)))
    for page_layout in extract_pages(pdf_file, laparams=LAParams()):
        print(f'Processing Page: {number_of_pages}')
        number_of_pages -= 1
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            if character.get_text() != ' ':
                                print(f"Character: {character.get_text()}")
                                print(f"Font Name: {character.fontname}")
                                print(f"Font Size: {character.size}")
                                print('\n')


def extract_character_colors(pdf_file):
    with pdfplumber.PDF(pdf_file) as file:
        for char in file.chars:
            if char['text'] != ' ':
                print(f"Page Number: {char['page_number']}")
                print(f"Character: {char['text']}")
                print(f"Font Name: {char['fontname']}")
                print(f"Font Size: {char['size']}")
                print(f"Stroking Color: {char['stroking_color']}")
                print(f"Non_stroking Color: {char['non_stroking_color']}")
                print('\n')


with open('ivi.pdf', 'rb') as scr_file:
    extract_character_characteristics(scr_file)
    extract_character_colors(scr_file)