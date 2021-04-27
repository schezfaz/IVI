from flask import Flask, jsonify, request, send_file
from flask_cors import CORS , cross_origin
import io

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
        file.save('./state/'+filename)
    return "Send Annoted PDF File"


@app.route('/returnFile', methods = ['GET'])
@cross_origin(support_credentials=True)
def returnFile():
    return send_file('/Users/bhavyameghnani/Desktop/IVI/misc/ivi.pdf')


app.run(port=5000, debug=True)