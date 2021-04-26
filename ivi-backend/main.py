from flask import Flask, jsonify, request, send_file
from flask_cors import CORS , cross_origin
import io
from operator import itemgetter
from PDFNetPython3 import PDFDoc, Text, Rect, SDFDoc, ColorPt
import fitz
import json

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, support_credentials=True)


@app.route('/')
@cross_origin(support_credentials=True)
def hello():
    return "Welcome to IVI by Team BaScheD!"


@app.route('/submitFile', methods = ['GET', 'POST'])
@cross_origin(support_credentials=True)
def submitFiles():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        print(filename)
    return send_file('/Users/bhavyameghnani/Desktop/IVI/misc/ivi.pdf')


@app.route('/returnFile', methods = ['GET'])
@cross_origin(support_credentials=True)
def returnFile():
    return send_file('/Users/bhavyameghnani/Desktop/IVI/misc/ivi.pdf')


@app.route('/signUp', methods = ['POST', 'GET'])
@cross_origin(support_credentials=True)
def signUp():
    return "done"


@app.route('/applyRules', methods = ['GET', 'POST'])
@cross_origin(support_credentials=True)
def applyRules():
    document = '../misc/EYResources/Input Sample.pdf'
    doc = fitz.open(document)
    pdfDoc = PDFDoc(document)
    styles, titles = extractData(doc, pdfDoc)
    for s in styles:
      print(s)

    print('Titles for every page')
    for t in titles:
      print(t)
    return 'Applied rules successfully!'


def addStickyNote(page, doc, pos):
  # Create the sticky note (Text annotation)
  # print('position',pos,int(pos[1]))
  txt = Text.Create( doc.GetSDFDoc(), Rect(pos[2]+5, 535 - pos[1], 1000, 0) )
  txt.SetIcon( "UserIcon" )
  txt.SetContents( "Text Not right, change it" )
  txt.SetColor( ColorPt(1,1,0) )
  txt.RefreshAppearance()
  page.AnnotPushBack( txt )

def extractData(doc, pdfDoc):
    styles = []
    titles_size = []
    titles_coordinates = []
    i=1
    for page in doc:
        print("Page:",i)
        page_annot = pdfDoc.GetPage(i)
        i=i+1
        blocks = page.getText("dict")["blocks"]
        max_size = 0
        min_cordinate = 999
        for b in blocks:  # iterate through the text blocks
            if b['type'] == 0:  # block contains text
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        filter = {'text':s['text'], 'size':s['size'], 'font':s['font'], 'color':hex(s['color']), 'bbox':s['bbox'], 'origin':s['origin'],'flags':s['flags']}
                        styles.append(filter)
                        # print("<-----",s,"---->")

                        if(max_size < s['size']):
                          max_size = s['size']
                          max_text_size = filter
                        
                        if(min_cordinate > s['bbox'][1]):
                          min_cordinate = s['bbox'][1]
                          min_text_coordinatee = filter
                        
                        addStickyNote(page_annot, pdfDoc, s['bbox'])
                                                  
        titles_size.append(max_text_size)
        print("Title on Size",max_text_size)
        
        titles_coordinates.append(min_text_coordinatee)
        print("Title on Coordinate",min_text_coordinatee)

    outfname =  "../output/new_annot_test_api.pdf"
    pdfDoc.Save(outfname, SDFDoc.e_linearized)

    return styles, titles_size

app.run(port=5000, debug=True)







# @app.route('/ppt')
# def ppt():
#     prs = Presentation('/Users/bhavyameghnani/Desktop/IVI/misc/ivi.pptx')
#     # text_runs will be populated with a list of strings,
#     # one for each text run in presentation
#     text_runs = []
#     for slide in prs.slides:
#         for shape in slide.shapes:
#             if not shape.has_text_frame:
#                 continue
#             for paragraph in shape.text_frame.paragraphs:
#                 for run in paragraph.runs:
#                     text_runs.append(run.text)
#     print(text_runs)
#     return "Check Console"


# @app.route('/ppt_font')
# def ppt_font():
#     prs = Presentation('/Users/bhavyameghnani/Desktop/IVI/misc/ivi.pptx')

#     # text_frame = shape.text_frame
#     # paragraph = text_frame.paragraphs[0]

#     for slide in prs.slides:
#         for shape in slide.shapes:
#             if not shape.has_text_frame:
#                 continue
#             for paragraph in shape.text_frame.paragraphs:
#                 for run in paragraph.runs:
#                     font = run.font
#                     try:
#                         font_size = font.size
#                         print(font_size)
#                         font_bold = font.bold
#                         print(font_bold)
#                         font_name = font.name
#                         print(font_name)
#                         # color = font.color.rgb
#                         # print(color)
#                     except:
#                         pass
#     return "Check Console"



# @app.route('/pdf')
# def pdf():
#     fd = open('/Users/bhavyameghnani/Desktop/IVI/misc/ivi.pdf', "rb")
#     doc = PDFDocument(fd)
#     page = next(doc.pages())
#     KEY = sorted(page.Resources.Font.keys())
#     print(KEY)
#     for i in range(len(KEY)):
#         font = page.Resources.Font[KEY[i]]
#         print("FONT SUBTYPE "+font.Subtype)
#         print("BASE FONT "+font.BaseFont)
#         print("FONT ENCODING "+font.Encoding)
#     return "Check Console"


# @app.route('/img')
# def img():
#     with tesserocr.PyTessBaseAPI() as api:
#         image = Image.open("/Users/bhavyameghnani/Desktop/IVI/misc/ivi.png")
#         api.SetImage(image)
#         api.Recognize()  # required to get result from the next line
#         iterator = api.GetIterator()
#         print(iterator.WordFontAttributes())
#     return "Check Console"


# @app.route('/plumber')
# def plumber():
#     pdf_file = pdfplumber.open('/Users/bhavyameghnani/Desktop/IVI/misc/ivi.pdf')
#     for p, char in zip(pdf_file.pages, pdf_file.chars):
#         words = p.extract_words(keep_blank_chars=True)
#         texts = p.extract_text()
#         # print(f"Page Number: {p.page_number}")
#         print(f"Font Name: {char['fontname']}")
#         print(f"Font Size: {char['size']}")
#         print(f"Stroking Color: {char['stroking_color']}")
#         print(f"Non_stroking Color: {char['non_stroking_color']}")
#         print(texts.strip())
#         print('\n')
#     return "Check Console"


# # def extract_character_characteristics(pdf_file):
# #     number_of_pages = len(list(extract_pages(pdf_file)))
# #     for page_layout in extract_pages(pdf_file, laparams=LAParams()):
# #         print(f'Processing Page: {number_of_pages}')
# #         number_of_pages -= 1
# #         for element in page_layout:
# #             if isinstance(element, LTTextContainer):
# #                 for text_line in element:
# #                     for character in text_line:
# #                         if isinstance(character, LTChar):
# #                             if character.get_text() != ' ':
# #                                 print(f"Character: {character.get_text()}")
# #                                 print(f"Font Name: {character.fontname}")
# #                                 print(f"Font Size: {character.size}")
# #                                 print('\n')
# #     return "Check Console"


# # def extract_character_colors(pdf_file):
# #     with pdfplumber.PDF(pdf_file) as file:
# #         for char in file.chars:
# #             if char['text'] != ' ':
# #                 print(f"Page Number: {char['page_number']}")
# #                 print(f"Character: {char['text']}")
# #                 print(f"Font Name: {char['fontname']}")
# #                 print(f"Font Size: {char['size']}")
# #                 print(f"Stroking Color: {char['stroking_color']}")
# #                 print(f"Non_stroking Color: {char['non_stroking_color']}")
# #                 print('\n')
# #     return "Check Console"


# @app.route('/plumber-update')
# def plumber_update():
#     with open('/Users/bhavyameghnani/Desktop/IVI/misc/ivi.pdf', 'rb') as scr_file:
#         extract_character_characteristics(scr_file)
#         extract_character_colors(scr_file)
#     return "Check Console"



    

# cd flask
# source bin/activate