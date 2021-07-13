from os import sendfile
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS , cross_origin
import io
from operator import itemgetter
# from PDFNetPython3 import PDFDoc, Text, Rect, SDFDoc, ColorPt
from elasticsearch import Elasticsearch
import json
import pandas
import Constants
import Config
import xlrd
# import boilerplate
from typing import Text
# import pdfplumber
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LAParams, LTTextLine
from elasticsearch import Elasticsearch
import Config
import Constants
from pdf_annotate import PdfAnnotator, Location, Appearance, Metadata
from pdf_annotate.config import constants
from pdf_annotate.graphics import ContentStream, Font, Save, BeginText, EndText, FillColor, Restore
from pdf_annotate.annotations.text import get_text_commands, FreeText

es = Elasticsearch(
    cloud_id=Config.CLOUD_ID,
    http_auth=(Config.USERNAME, Config.PASSWORD),
    ) 

#:chg: global vars
x1 = []
y1 = []
x2 = []
y2 = []
element = []
error = []
pageNo = []
result_annotation = {}
blockToText = {}


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, support_credentials=True)


@app.route('/')
@cross_origin(support_credentials=True)
def hello():
    return "Welcome to IVI by Team BaScheD!"

# return the processed file
@app.route('/returnFile', methods = ['GET'])
@cross_origin(support_credentials=True)
def returnFile():
    return send_file('output_annoted.pdf')

# Analyse file
@app.route('/submitFile', methods = ['GET', 'POST'])
@cross_origin(support_credentials=True)
def submitFiles():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        print(filename)
        print(request.form['brandGuideline'])
        file.save('./state/'+filename)
        # Call Apply Rules Func
        #outfname = applyRules(request.form['brandGuideline'], filename)
        
        extractData('state/'+filename) #calling new method:chg
    # return "Send Annoted PDF File"
    #return outfname
    return "Your file has been analyzed successfully!"

@app.route('/addBrandGuideline', methods = ['GET', 'POST'])
@cross_origin(support_credentials=True)
def addBrandGuideline():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        print(filename)
        file.save('./guidelines/'+filename)
        # Call Apply Rules Func
        outfname = extractRules(filename)
    # return "Send Annoted PDF File"
    return outfname

def extractRules(document):
    wb = xlrd.open_workbook(document)
    sheet = wb.sheet_by_index(0)
    rules = {}
    rowCount = sheet.nrows
    for i in range(1,rowCount):
        element = sheet.cell_value(i,0)
        element_rule = sheet.cell_value(i,1)
        parameterRules = {}
        for rule in element_rule.split("\n"):
            parameter = rule.split(":")[0].strip()
            value = rule.split(":")[1].strip()
            parameterRules[parameter] = value
        rules[element] = parameterRules

    #store rules in EL

    return rules


#:chg: adding u_p extractData method
def extractData(pdf_file):
    templateName = "Nomura"
    template = es.get(index="template", id=templateName)
    template_boilerplate = es.get(index="boilerplate", id=templateName+'_boilerplate')
    template_data = template["_source"][templateName]
    template_boilerplate_data = template_boilerplate["_source"][templateName]
    boilerPlateText = [x.strip() for x in open('./boilerplate/boilerplate.txt').readlines()]
    for ind,text in  enumerate(boilerPlateText):
        blockToText[ind] = text  
    a = PdfAnnotator(pdf_file)
    extract_character_characteristics(a, pdf_file, template_data, template_boilerplate_data)
    a.write('output_annoted.pdf') 
    es.index(index="annotation", body=result_annotation,id="Demo")
    return 

#:chg u_p: extract_character_characteristics
def extract_character_characteristics(a, pdf_file, template_data, template_boilerplate_data):
    flag_char_disperancies = 0
    font_rules = template_data[Constants.TEXT_FONT][Constants.RULES]
    bullet_rules = template_data[Constants.BULLET][Constants.RULES]
    boilerplate_rules = template_data[Constants.BOILERPLATE_TEXT][Constants.RULES]
    page_counter = -1
    number_of_pages = len(list(extract_pages(pdf_file)))
    # iterating over pages in teh pdf
    for page_layout in extract_pages(pdf_file, laparams=LAParams()):
        print(f'Processing Page: {page_counter+1}')
        #number_of_pages -= 1
        page_counter += 1
        max_size = 10
        prev_bullet_level = 0
        prev_bullet_position = 0
        boilerplate_text_count = 0
        for element in page_layout:
            #checking if its a textbox
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    prev_bullet = False
                    #For last slide for boilerplate check
                    if(page_counter == number_of_pages-1): 
                        if boilerplate_text_count in blockToText.keys():
                            if text_line.get_text().lower().strip() != blockToText[boilerplate_text_count].lower().strip():
                                annotation(a, pdf_file, text_line.bbox[0], text_line.bbox[1], text_line.bbox[2], text_line.bbox[3], "BoilerPlate", "not matching" , page_counter)  
                            boilerplate_text_count += 1
                        
                    # if isinstance(text_line, LTTextLine):
                    #     print("%6d, %6d, %s" % (text_line.bbox[0], text_line.bbox[1], text_line.get_text().replace('\n', '_')))
                    for character in text_line :
                        if isinstance(character, LTChar) and page_counter != number_of_pages-1:
                            if character.get_text() != ' ':
                                # print(f"Character: {character.get_text()}")
                                # print(f"Font Name: {character.fontname}")
                                # print(f"Font Size: {character.size}")
                                # print('\n')
                                # print(font_rules[Constants.PARAGRAPH_FONT_STYLE])
                                # checking font style 
                                if font_rules[Constants.PARAGRAPH_FONT_STYLE].strip().lower() not in character.fontname.lower():
                                    # print("Text Font Font style should be "+font_rules[Constants.PARAGRAPH_FONT_STYLE]+", current style:"+character.fontname)
                                    fontname_error = "Text Font Font style should be "+font_rules[Constants.PARAGRAPH_FONT_STYLE]+", current style:"+character.fontname
                                    flag_char_disperancies = 1
                                    fontname_line = text_line

                                #checking bullet indentation
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
                                        annotation(a, pdf_file, text_line.bbox[0], text_line.bbox[1], text_line.bbox[2], text_line.bbox[3], "Bullet", bullet_error , page_counter)
                                    prev_bullet = False
                                    continue

                                # determining header text
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

                # checking header font rules
                error = ""                        
                heading_rules = template_data[Constants.STANDARD_PAGE_HEADING][Constants.RULES]
                if(int(heading_rules["Font Size"].strip().split(' ')[0]) != round(max_size)):
                    error += "Font size should be "+heading_rules["Font Size"].strip().split(' ')[0]+", current size:"+str(round(max_size))
                    error += "\n"
                if heading_rules["Font style"].strip().lower() not in header_font.lower():
                    error += "Font style should be "+heading_rules["Font style"]+", current style:"+header_font


        print("------------")
        if page_counter != number_of_pages-1:
            if error != '':
                annotation(a, pdf_file, header_text_line.bbox[0], header_text_line.bbox[1], header_text_line.bbox[2], header_text_line.bbox[3], "Heading", error , page_counter)
            # print(line.bbox[0])
            if(flag_char_disperancies == 1):
                flag_char_disperancies = 0
                annotation(a, pdf_file, fontname_line.bbox[0], fontname_line.bbox[1], fontname_line.bbox[2], fontname_line.bbox[3], "Fontname", fontname_error , page_counter)

#:chg: annotation
def annotation(a, pdf_file, x1, y1, x2, y2, element, error, pageNo):
    a.add_annotation(
        'square',
        Location(x1=x1, y1=y1, x2=x2, y2=y2, page=pageNo),
        Appearance(stroke_color=(1, 0, 0), stroke_width=1),
    )
    a.add_annotation(
        'text',
        Location(x1=x1, y1=y1+12, x2=x2, y2=y2+15, page=pageNo),
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
    


@app.route('/saveTemplate/<templateName>', methods = ['GET', 'POST'])
@cross_origin(support_credentials=True)
def saveTemplateToDB(templateName):
  excel_data_df = pandas.read_excel('../misc/EYResources/Brand guidelines.xlsx', sheet_name='Typography brand Guidelines')

  json_str = excel_data_df.to_json()
  template = json.loads(json_str)

  defined_headers = ['Sub Element','Rules','Exception']
  dict = {}

  # print(template.keys())
  print('Excel Sheet to JSON:\n', template.keys())
  for key in template.keys():
    if key in defined_headers:
      for i in template[key]:
        if(key == 'Sub Element'):
          dict[i] = template[key][i].strip()

  for key in template.keys():
    if key in defined_headers:    
      for i in template[key]:
        if(key == 'Rules'):
          temp = dict[i]
          dict[temp] = {}
          
          rules_list = template[key][i].split('\n')
          rule_dict = {}
          for rule in rules_list:  
            key_val = rule.split(":")
            if(len(key_val) == 2):      
              rule_dict[key_val[0].strip()] = key_val[1].strip()
            
          dict[temp]["Rules"] = rule_dict


  for key in template.keys():
    if key in defined_headers:
      for i in template[key]:
        if(key == 'Exception'):
          # print(template[key][i])
          temp = dict[i]
          del dict[i]
          dict[temp]["Exception"] = template[key][i]

  template_dict = {}
  template_dict[templateName] = dict
  es.index(index="template", body=template_dict,id=templateName)
  return json.dumps(template_dict,indent=4)

@app.route('/addBoilerPlate/<templateName>', methods = ['GET', 'POST'])
@cross_origin(support_credentials=True)
def saveBoilerPlateToDB(templateName):
  blockToText = {}
  boilerPlateText = [x.strip() for x in open('./boilerplate/boilerplate.txt').readlines()]
  for ind,text in  enumerate(boilerPlateText):
    blockToText[ind+1] = text
  
  temp = {}
  temp[templateName]=blockToText
  es.index(index="boilerplate", body=temp,id=templateName+'_boilerplate')
  return json.dumps(temp,indent=4)

app.run(port=5000, debug=True)
