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
        file.save('./state/'+filename)
        # Call Apply Rules Func
        outfname = applyRules()
    # return "Send Annoted PDF File"
    return outfname


# @app.route('/applyRules', methods = ['GET', 'POST'])
# @cross_origin(support_credentials=True)
def applyRules():
    document = '../misc/EYResources/Input Sample.pdf'
    doc = fitz.open(document)
    pdfDoc = PDFDoc(document)
    styles, titles, outfname = extractData(doc, pdfDoc)
    for s in styles:
      print(s)

    print('Titles for every page')
    for t in titles:
      print(t)
    return outfname
    # return 'Applied rules successfully!'
    # return send_file(outfname)


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

    return styles, titles_size, outfname

app.run(port=5000, debug=True)
