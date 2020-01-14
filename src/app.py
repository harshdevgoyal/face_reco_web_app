import numpy as np
import yaml
import sys
from io import BytesIO
from typing import List, Dict, Union, ByteString, Any
import os
import flask
from flask import Flask
import matplotlib.pyplot as plt
import cv2
import requests
import json
import face_recognition
from PIL import Image,ImageDraw
import concurrent.futures
import multiprocessing

path= os.path.dirname(os.path.realpath(__file__))+'/'


with open(path+"config.yaml", 'r') as stream:
    APP_CONFIG = yaml.full_load(stream)


app = Flask(__name__)


unknown_face_distances=None
unknown_face_encodings=None
known_face_encodings=[]
known_face_names=[]
unknown_image=None
#small_images=[]

w,l=200,150
org = (10, 50) 
fontScale = 1.8 
# Blue color in BGR 
color = (255, 0, 0) 
# Line thickness of 2 px 
thickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX 


def get_best_matches():

    face_distances=[]

    for face_encoding in  unknown_face_encodings:
        face_distances.append(face_recognition.face_distance(known_face_encodings, face_encoding))
    face_distances=np.asarray(face_distances)

    unknown,known=face_distances.shape

    sorted_known=np.argsort(face_distances,axis=-1)
    sorted_distances=np.sort(face_distances,axis=-1)
    count=np.full(unknown,0)    

    best_known=sorted_known[np.arange(unknown),count]
    distance_known=sorted_distances[np.arange(unknown),count]

    flag=True
    #Handling duplicates
    while flag:
        u,c=np.unique(best_known[best_known!=1000],return_counts=True)
        
        if np.sum(c>1)==0:
            break
            
        for i in u[c>1]:
            locs=np.argwhere(best_known==i)
            dists=distance_known[locs]

            locs=np.delete(locs,np.argmin(dists))
            for loc in locs:
                if count[loc]<known-1:
                    count[loc]+=1
                    distance_known[loc]=sorted_distances[loc,count[loc]]
                    best_known[loc]=sorted_known[loc,count[loc]]
                elif count[loc]==known-1:
                    best_known[loc]=1000
    
    return best_known,distance_known
                
       


def get_output():
    
    best_known,distance_known=get_best_matches()
    tolerance=0.5
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance  to draw with
    draw = ImageDraw.Draw(pil_image)

    for (top, right, bottom, left), idx,distance in zip(unknown_face_locations, best_known, distance_known):
        
        if idx==1000 or distance>tolerance:
            name='__'
        else:
            name=known_face_names[idx]
            
    # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
        
    # Remove the drawing library from memory as per the Pillow docs
    del draw

    pil_image.save(path+'static/output.jpg')
                 

def create_unknown_face_encodings(raw_bytes: ByteString):
    global unknown_image
    #print(type(BytesIO(raw_bytes)))
    unknown_image=face_recognition.load_image_file(BytesIO(raw_bytes))
    unknown_face_locations = face_recognition.face_locations(unknown_image)
    unknown_face_encodings=face_recognition.face_encodings(unknown_image,unknown_face_locations)
    return unknown_face_locations,unknown_face_encodings

# def create_small_image(image,name):
#     res = cv2.resize(image, dsize=(w, l), interpolation=cv2.INTER_CUBIC)
#     image = cv2.putText(res,name, org, font,  
#                         fontScale, color, thickness, cv2.LINE_AA)
#     small_images.append(image)
    

# def create_known_face_encodings(raw_bytes: ByteString):
#     known_image=face_recognition.load_image_file(BytesIO(raw_bytes))
#     known_face_images.append(known_image)
#     face_encodings=face_recognition.face_encodings(known_image)
#     #create_small_image(known_image,name)
#     return face_encodings[0]


def make_image_array(known_face_names,known_face_images):

    n=len(known_face_names)
    c=int(1000/w)
    r=int(np.ceil(n/c))

    img_array=np.zeros((r*l,c*w,3))
    for i,image in enumerate(known_face_images):
        res = cv2.resize(image, dsize=(w, l), interpolation=cv2.INTER_CUBIC)
        name=known_face_names[i]
        image = cv2.putText(res,name, org, font,  
                            fontScale, color, thickness, cv2.LINE_AA)
        img_array[i//c*l:(i//c+1)*l,i%c*w:(i%c+1)*w,:]=image
    #print(len(small_images))    
    img_array=img_array.astype(int)
    plt.imsave(path+'static/array.jpg', img_array/255)

    #del known_face_images


@app.route('/api/upload_group_pic', methods=['POST'])
def upload_group_pic():
    file=flask.request.files['file']
    filename=file.filename
    bytes = file.read()
    # print(bytes)
    global unknown_face_locations
    global unknown_face_encodings
    unknown_face_locations,unknown_face_encodings=create_unknown_face_encodings(bytes)
    #print(os.path.splitext(filename)[0])
    print(f'No of unknown encodings:{len(unknown_face_encodings)}')
    return f'No of unknown encodings:{len(unknown_face_encodings)}'


def process_ind_image(image):
    #filename=file.filename
        #bytes=file.read()
        #known_face_names.append(os.path.splitext(filename)[0])
        # name=str(i)
        # i=i+1
        # known_face_names.append(name)
        #known_face_encodings.append(create_known_face_encodings(bytes))
        return face_recognition.face_encodings(image)[0]


@app.route('/api/upload_ind_pics', methods=['POST'])
def upload_ind_pic():
  
    #global known_face_images
    global known_face_encodings
    global known_face_names
    known_face_encodings=[]
    #known_face_names=[]
    known_face_images=[]
    # global small_images
    # small_images=[]
    files = flask.request.files.getlist('file')

    for file in files:
        known_face_images.append(face_recognition.load_image_file(BytesIO(file.read())))
    #print(len(known_face_images),known_face_images[0],type(known_face_images[0]))
    # with concurrent.futures.ProcessPoolExecutor as executor:
    #     encodings=executor.map(process_ind_image,files)
    # #for i,file in enumerate(files):
    #     for encoding in encodings:
    #         known_face_encodings.append(encoding)

    # 
    known_face_names=list(map(str,np.arange(len(known_face_images))))
    # for image in known_face_images:
    #     known_face_encodings.append(process_ind_image(image))
    p=multiprocessing.Pool()
    known_face_encodings=p.map(process_ind_image,known_face_images) 
    p.close()

    make_image_array(known_face_names,known_face_images)
    print(f'No of known encodings:{len(known_face_encodings)}')
    print(known_face_names)
    print(len(known_face_encodings),known_face_encodings[0].shape)
    return f'No of known encodings:{len(known_face_encodings)}'

    #return 'success'
    

@app.route('/api/recognize')
def recognize():

    get_output()
    return 'success'
    #url=flask.url_for('static', filename='output.jpg')
    
    #print(url)
    # return flask.send_file(path+'static/output.jpg',
    #                   mimetype='image/jpg',
    #                   attachment_filename='output.jpg',
    #                   as_attachment=True)

    # return flask.send_file(
    # get_output(),
    # mimetype='image/jpeg',
    # as_attachment=True,
    # attachment_filename='output.jpg')


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
    port = os.environ.get('PORT', 8000)

    if "prepare" not in sys.argv:
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        #app.run(debug=True, port=5000)
        app.run(host='0.0.0.0', port=port,debug=True)