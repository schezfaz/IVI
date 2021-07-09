from typing import Text
import pdfplumber
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LAParams, LTTextLine
from elasticsearch import Elasticsearch
import Config
import Constants
from pdfrw import PdfReader
from pdf_annotate import PdfAnnotator, Location, Appearance, Metadata
from pdf_annotate.config import constants
from pdf_annotate.graphics import ContentStream, Font, Save, BeginText, EndText, FillColor, Restore
from pdf_annotate.annotations.text import get_text_commands, FreeText

es = Elasticsearch(
    cloud_id=Config.CLOUD_ID,
    http_auth=(Config.USERNAME, Config.PASSWORD),
) 
a = PdfAnnotator('Input Sample.pdf')
result_annotation = {}

def extractData(pdf_file):
    templateName = "Nomura"
    template = es.get(index="template", id=templateName)
    template_boilerplate = es.get(index="boilerplate", id=templateName+'_boilerplate')
    template_data = template["_source"][templateName]
    template_boilerplate_data = template_boilerplate["_source"][templateName]
    extract_character_characteristics(pdf_file, template_data, template_boilerplate_data)
    # print(result_annotation)
    es.index(index="annotation", body=result_annotation,id="Demo")

    a.write('b.pdf') 
    return 

def extract_character_characteristics(pdf_file, template_data, template_boilerplate_data):

    flag_char_disperancies = 0
    font_rules = template_data[Constants.TEXT_FONT][Constants.RULES]
    bullet_rules = template_data[Constants.BULLET][Constants.RULES]
    boilerplate_rules = template_data[Constants.BOILERPLATE_TEXT][Constants.RULES]
    
    page_counter = -1
    number_of_pages = len(list(extract_pages(pdf_file)))
    for page_layout in extract_pages(pdf_file, laparams=LAParams()):
        print(f'Processing Page: {number_of_pages}')
        number_of_pages -= 1
        page_counter += 1
        max_size = 10
        prev_bullet_level = 0
        prev_bullet_position = 0
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    prev_bullet = False
                    # if isinstance(text_line, LTTextLine):
                    #     print("%6d, %6d, %s" % (text_line.bbox[0], text_line.bbox[1], text_line.get_text().replace('\n', '_')))
                    for character in text_line:
                        if isinstance(character, LTChar):
                            if character.get_text() != ' ':
                                # print(f"Character: {character.get_text()}")
                                # print(f"Font Name: {character.fontname}")
                                # print(f"Font Size: {character.size}")
                                # print('\n')
                                # print(font_rules[Constants.PARAGRAPH_FONT_STYLE])
                                if font_rules[Constants.PARAGRAPH_FONT_STYLE].strip().lower() not in character.fontname.lower():
                                    # print("Text Font Font style should be "+font_rules[Constants.PARAGRAPH_FONT_STYLE]+", current style:"+character.fontname)
                                    fontname_error = "Text Font Font style should be "+font_rules[Constants.PARAGRAPH_FONT_STYLE]+", current style:"+character.fontname
                                    flag_char_disperancies = 1
                                    fontname_line = text_line

                                if character.get_text() in Constants.BULLET_SAMPLE:
                                    prev_bullet = True 
                                    if not prev_bullet_position:
                                        prev_bullet_position = text_line.bbox[0]
                                        prev_bullet_level = 1
                                    else:
                                        if (prev_bullet_position != text_line.bbox[0]):
                                            prev_bullet_level = prev_bullet_level + 1
                                        else:
                                            prev_bullet_level = 1
                                    print("BULLET",character.get_text(), prev_bullet_level)
                                    continue
                                
                                
                                if prev_bullet:
                                    bullet_error = ''
                                    bullet_rule = bullet_rules['Level '+str(prev_bullet_level)].strip().split(' ')
                                    
                                    if bullet_rule[0].strip().lower() not in character.fontname.lower():
                                        bullet_error += "Font style should be "+bullet_rule[0]+", current style:"+character.fontname
                                        bullet_error += '\n'
                                    if(int(bullet_rule[1].strip()) != round(character.size)):
                                        bullet_error += "Font size should be "+bullet_rule[1].strip()+", current size:"+str(round(character.size))
                                    
                                    if bullet_error != '':
                                        print("ERRROR",bullet_error)
                                    # addStickyNote(page_annot, pdfDoc, filter['bbox'], "Bullet", bullet_error)
                                        annotation(text_line.bbox[0], text_line.bbox[1], text_line.bbox[2], text_line.bbox[3], "Bullet", bullet_error , page_counter)
                                    prev_bullet = False
                                    continue


                                if(max_size < int(character.size)):
                                    max_size = int(character.size)
                                    # max_text_size = filter
                                    # line = text_line
                                    print(text_line)
                                    print(int(character.size))
                                    print(int(max_size))
                                    # print(type(character.size))
                                    header_font = character.fontname
                                    header_text_line = text_line
                                    
                error = ""                        
                heading_rules = template_data[Constants.STANDARD_PAGE_HEADING][Constants.RULES]
                if(int(heading_rules["Font Size"].strip().split(' ')[0]) != round(max_size)):
                    error += "Font size should be "+heading_rules["Font Size"].strip().split(' ')[0]+", current size:"+str(round(max_size))
                    error += "\n"
                if heading_rules["Font style"].strip().lower() not in header_font.lower():
                    error += "Font style should be "+heading_rules["Font style"]+", current style:"+header_font

        print("---")
            
        if error != '':
            annotation(header_text_line.bbox[0], header_text_line.bbox[1], header_text_line.bbox[2], header_text_line.bbox[3], "Heading", error , page_counter)
        # print(line.bbox[0])
        if(flag_char_disperancies == 1):
            flag_char_disperancies = 0
            # print("darshan")
            annotation(fontname_line.bbox[0], fontname_line.bbox[1], fontname_line.bbox[2], fontname_line.bbox[3], "Fontname", fontname_error , page_counter)


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


def annotation(x1, y1, x2, y2, element, error, pageNo):
    a.add_annotation(
        'square',
        Location(x1=x1, y1=y1, x2=x2, y2=y2, page=pageNo),
        Appearance(stroke_color=(1, 0, 0), stroke_width=2),
    )
    a.add_annotation(
        'text',
        Location(x1=x1, y1=y1, x2=x2, y2=y2, page=pageNo),
        Appearance(
            fill=[0.4, 0, 0],
            stroke_width=1,
            font_size=10,
            content=element + " : "+ error,
        ),
    )
    annotation_parameters = {}
    annotation_parameters["X1"] = str(x1)
    annotation_parameters["X2"] = str(x2)
    annotation_parameters["Y1"] = str(y1)
    annotation_parameters["Y2"] = str(y2)
    annotation_parameters["Element"] = element
    annotation_parameters["Error"] = error
    annotation_parameters_list = [annotation_parameters]
    if pageNo not in result_annotation.keys():
        result_annotation[pageNo] = annotation_parameters_list
    else:
        result_annotation[pageNo].extend(annotation_parameters_list)

    
with open('Input Sample.pdf', 'rb') as scr_file:
    extractData(scr_file)
    # extract_character_characteristics(scr_file)
    # extract_character_colors(scr_file)
    # reader = PdfReader('Bullet_test.pdf')
    # print(reader.Info.Title)
