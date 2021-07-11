from os import sendfile
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


def checkBoilerPlate(doc, pdfDoc, template_boilerplate_data):
    styles = []
    i=1
    block_no=0
    page = doc[len(doc)-1]
    blocks = page.getText("dict")["blocks"]
    page_annot = pdfDoc.GetPage(len(doc))
    for b in blocks:  # iterate through the text blocks
              if b['type'] == 0:
                   block_no = block_no+1
                   line_text=''
                   for l in b["lines"]: # iterate through the text lines    
                      for s in l["spans"]:  # iterate through the text spans
                          filter = {'text':s['text'], 'size':s['size'], 'font':s['font'], 'color':hex(s['color']), 'bbox':s['bbox'], 'origin':s['origin'],'flags':s['flags']}
                          styles.append(filter)
                          line_text+=s['text']
                          pos=s['bbox']
                   print(block_no,"--> ",line_text)
                   if template_boilerplate_data[str(block_no)].strip().lower() != line_text.strip().lower():
                       addStickyNote(page_annot, pdfDoc, pos, "Boilerplate","Not matching, should be:"+template_boilerplate_data[str(block_no)])
                                      

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


