import numpy as np
import yaml
import sys
from io import BytesIO
from typing import List, Dict, Union, ByteString, Any
import os
import flask
from flask import Flask
import matplotlib.pyplot as plt
import requests
import json
import shutil 
import face_recognition
import os
from PIL import Image,ImageDraw



with open("config.yaml", 'r') as stream:
    APP_CONFIG = yaml.full_load(stream)


app = Flask(__name__)

unknown_face_distances=None
unknown_face_encodings=None
known_face_encodings=[]
known_face_names=[]
unknown_image=None

def create_unknown_face_encodings(raw_bytes: ByteString):
    global unknown_image
    print(type(BytesIO(raw_bytes)))
    unknown_image=face_recognition.load_image_file(BytesIO(raw_bytes))
    unknown_face_locations = face_recognition.face_locations(unknown_image)
    unknown_face_encodings=face_recognition.face_encodings(unknown_image,unknown_face_locations)
    return unknown_face_locations,unknown_face_encodings

def create_known_face_encodings(raw_bytes: ByteString):
    known_image=face_recognition.load_image_file(BytesIO(raw_bytes))
    known_face_encodings=face_recognition.face_encodings(known_image)
    return known_face_encodings[0]

def get_output():
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance  to draw with
    draw = ImageDraw.Draw(pil_image)
    # Loop through each face found in the unknown image

    for (top, right, bottom, left), face_encoding in zip(unknown_face_locations, unknown_face_encodings):

        
        # See if the face is a match for the known face(s)
        #matches = face_recognition.face_distance(known_face_encodings, face_encoding)
        
        name = "__"

        # Or instead, use the known face with the smallest distance to the new face

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        # ind=np.argsort(face_distances)
        # distances.append(face_distances[ind])
        # names.append(np.array(known_face_names)[ind])
        # indexes.append(i)

        #if min(face_distances)<=0.55:
        best_match_index = np.argmin(face_distances)
        name = known_face_names[best_match_index]
            
        #if matches[best_match_index]:

        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
        
    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Display the resulting image
    #pil_image.save(directory+'output.jpg')

    # b=BytesIO()
    # pil_image=pil_image.resize((512,512))
    # pil_image.save(b,'jpeg')
    # return b
    print(type(pil_image))
    pil_image.save('./static/output.jpg')
   #return flask.send_file(flask.url_for()'output.jpg',mimetype='image/jpg')
    #display(pil_image)


@app.route('/api/upload_group_pic', methods=['POST'])
def upload_group_pic():
    file=flask.request.files['file']
    filename=file.filename
    bytes = file.read()
    # print(bytes)
    global unknown_face_locations
    global unknown_face_encodings
    unknown_face_locations,unknown_face_encodings=create_unknown_face_encodings(bytes)
    print(os.path.splitext(filename)[0])
    print(f'No of unknown encodings:{len(unknown_face_encodings)}')
    return f'No of unknown encodings:{len(unknown_face_encodings)}'

@app.route('/api/upload_ind_pics', methods=['POST'])
def upload_ind_pic():
    files = flask.request.files.getlist('file')
    # print(type(images[0]))
    # print(images[0].read())
   
    global known_face_encodings
    global known_face_names
    known_face_encodings=[]
    known_face_names=[]
    for file in files:
        filename=file.filename
        bytes=file.read()
        known_face_names.append(os.path.splitext(filename)[0])
        known_face_encodings.append(create_known_face_encodings(bytes))
   
    print(f'No of known encodings:{len(known_face_encodings)}')
    print(known_face_names)

    return f'No of known encodings:{len(known_face_encodings)}'


@app.route('/api/recognize')
def recognize():

    get_output()
    #url=flask.url_for('static', filename='output.jpg')

    #print(url)
    return 'success'

    # return flask.send_file(
    # get_output(),
    # mimetype='image/jpeg',
    # as_attachment=True,
    # attachment_filename='output.jpg')

# @app.route('/api/classify', methods=['POST', 'GET'])
# def upload_file():
#     if flask.request.method == 'GET':
#         url = flask.request.args.get("url")
#         img = load_image_url(url)
#     else:
#         bytes = flask.request.files['file'].read()
#         img = load_image_bytes(bytes)
#     #res = predict(img)
#     return flask.jsonify(res)


# @app.route('/api/classes', methods=['GET'])
# def classes():
#     #classes = sorted(model.data.classes)
#     return flask.jsonify('f')


@app.route('/ping', methods=['GET'])
def ping():
    # pil_image=Image.open('sample.jpg')
    # pil_image.save('/static/output.jpg')
    return os.getcwd()



@app.route('/config')
def config():
    return flask.jsonify(APP_CONFIG)


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    response.cache_control.max_age = 0
    return response


@app.route('/<path:path>')
def static_file(path):
    if ".js" in path or ".css" in path:
        return app.send_static_file(path)
    else:
        return app.send_static_file('index.html')


@app.route('/')
def root():
    return app.send_static_file('index.html')


def before_request():
    app.jinja_env.cache = {}


#model = load_model('models')

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)

    if "prepare" not in sys.argv:
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(debug=True, host='0.0.0.0', port=port)
        # app.run(host='0.0.0.0', port=port)