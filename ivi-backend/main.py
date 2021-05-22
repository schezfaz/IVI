from flask import Flask, jsonify, request, send_file
from flask_cors import CORS , cross_origin
import io
from operator import itemgetter
from PDFNetPython3 import PDFDoc, Text, Rect, SDFDoc, ColorPt
import fitz
from elasticsearch import Elasticsearch
import json
import pandas
import Constants
import Config
import xlrd

es = Elasticsearch(
    cloud_id=Config.CLOUD_ID,
    http_auth=(Config.USERNAME, Config.PASSWORD),
    ) 


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, support_credentials=True)


@app.route('/')
@cross_origin(support_credentials=True)
def hello():
    return "Welcome to IVI by Team BaScheD!"


@app.route('/returnFile', methods = ['GET'])
@cross_origin(support_credentials=True)
def returnFile():
    return send_file('/Users/bhavyameghnani/Desktop/IVI/misc/ivi.pdf')


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
        outfname = applyRules(request.form['brandGuideline'])
    # return "Send Annoted PDF File"
    return outfname

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

@app.route('/applyRules/<templateName>', methods = ['GET', 'POST'])
@cross_origin(support_credentials=True)
def applyRules(templateName):
    document = '../misc/EYResources/Input Sample.pdf'
    doc = fitz.open(document)
    pdfDoc = PDFDoc(document)
    template = es.get(index="template", id=templateName)
    template_data = template["_source"][templateName]

    styles, titles, outfname = extractData(doc, pdfDoc, template_data)
    # for s in styles:
    #   print(s)

    # print('Titles for every page')
    # for t in titles:
    #   print(t)
    return outfname
    # return 'Applied rules successfully!'
    # return send_file(outfname)


def extractData(doc, pdfDoc, template_data):
    styles = []
    titles_size = []
    titles_coordinates = []
    i=1
    for page in doc:
        if(len(doc) > 1 and page!=1):
          print("Page:",i)
          page_annot = pdfDoc.GetPage(i)
          i=i+1
          blocks = page.getText("dict")["blocks"]
          max_size = 0
          min_cordinate = 999
          prev_bullet_level = 0
          prev_bullet_position = 0
          for b in blocks:  # iterate through the text blocks
              if b['type'] == 0:  # block contains text
                  prev_bullet = False 
                  for l in b["lines"]: # iterate through the text lines 
                      for s in l["spans"]:  # iterate through the text spans
                          filter = {'text':s['text'], 'size':s['size'], 'font':s['font'], 'color':hex(s['color']), 'bbox':s['bbox'], 'origin':s['origin'],'flags':s['flags']}
                          styles.append(filter)
                          # print("<-----",s,"---->")
                          # fetching para font rules and applied
                          font_rules = template_data[Constants.TEXT_FONT][Constants.RULES]
                          bullet_rules = template_data[Constants.BULLET][Constants.RULES]
                          boilerplate_rules = template_data[Constants.BOILERPLATE_TEXT][Constants.RULES]
                          
                          if filter['text'] in Constants.BULLET_SAMPLE:
                            prev_bullet = True 
                            if not prev_bullet_position:
                              prev_bullet_position = filter['origin'][0]
                              prev_bullet_level = 1
                            else:
                              if (prev_bullet_position != filter['origin'][0]):
                                prev_bullet_level = prev_bullet_level + 1
                              else:
                                prev_bullet_level = 1
                            print("BULLET",filter['text'], prev_bullet_level)
                            continue
                          
                          if prev_bullet:
                            bullet_error = ''
                            bullet_rule = bullet_rules['Level '+str(prev_bullet_level)].strip().split(' ')
                            if bullet_rule[0].strip().lower() not in filter['font'].lower():
                              bullet_error += "Font style should be "+bullet_rule[0]+", current style:"+filter['font']
                              bullet_error += '\n'
                            if(int(bullet_rule[1].strip()) != round(filter['size'])):
                              bullet_error += "Font size should be "+bullet_rule[1].strip()+", current size:"+str(round(filter['size']))
                            
                            if bullet_error != '':
                              addStickyNote(page_annot, pdfDoc, filter['bbox'], "Bullet", bullet_error)
                            continue


                          if font_rules[Constants.PARAGRAPH_FONT_STYLE].strip().lower() not in filter['font'].lower():
                            addStickyNote(page_annot, pdfDoc, filter['bbox'],"Text Font", "Font style should be "+font_rules[Constants.PARAGRAPH_FONT_STYLE]+", current style:"+filter['font']) 

                          if(max_size < s['size']):
                            max_size = s['size']
                            max_text_size = filter
                          
                          if(min_cordinate > s['bbox'][1]):
                            min_cordinate = s['bbox'][1]
                            min_text_coordinatee = filter
                          
          # fetching heading rules and applied
          error = ''
          heading_rules = template_data[Constants.STANDARD_PAGE_HEADING][Constants.RULES]
          if(int(heading_rules["Font Size"].strip().split(' ')[0]) != round(max_text_size['size'])):
            error += "Font size should be "+heading_rules["Font Size"].strip().split(' ')[0]+", current size:"+str(round(max_text_size['size']))
            error += "\n"
          if heading_rules["Font style"].strip().lower() not in max_text_size['font'].lower():
            error += "Font style should be "+heading_rules["Font style"]+", current style:"+max_text_size['font']
            
          if error != '':
            addStickyNote(page_annot, pdfDoc, max_text_size['bbox'], "Heading", error)

          # checking heading with a. Max text size b. Top most coordinate on the page
          titles_size.append(max_text_size)
          #print("Title on Size",max_text_size)
          titles_coordinates.append(min_text_coordinatee)
          #print("Title on Coordinate",min_text_coordinatee)

    outfname =  "../output/new_annot_test_api.pdf"
    pdfDoc.Save(outfname, SDFDoc.e_linearized)

    return styles, titles_size, outfname


def addStickyNote(page, doc, pos, element, error):
  # Create the sticky note (Text annotation)
  # print('position',pos,int(pos[1]))
  # creating a note using offset
  txt = Text.Create( doc.GetSDFDoc(), Rect(pos[2]+Constants.X_COORDINATE_OFFSET, Constants.Y_COORDINATE_OFFSET - pos[1], 1000, 0) )
  txt.SetIcon( "UserIcon" )
  txt.SetContents( element+":"+ error)
  txt.SetColor( ColorPt(1,1,0) )
  txt.RefreshAppearance()
  page.AnnotPushBack( txt )


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



app.run(port=5000, debug=True)
