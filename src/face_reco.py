import face_recognition
import shutil
import numpy as np
#import pandas as pd 
# import cv2
import glob
from PIL import Image, ImageDraw
import os
#from IPython.display import display
#import matplotlib.pyplot as plt
from typing import List, Dict, Union, ByteString, Any
from io import BytesIO
import time
# from skimage import io
# import imageio

def create_unknown_face_encodings(raw_bytes: ByteString):
    unknown_image=face_recognition.load_image_file(BytesIO(raw_bytes))
    unknown_face_locations = face_recognition.face_locations(unknown_image)
    unknown_face_encodings=face_recognition.face_encodings(unknown_image,unknown_face_locations)
    return unknown_face_locations,unknown_face_encodings

def create_known_face_encodings(raw_bytes: ByteString):
    known_image=face_recognition.load_image_file(BytesIO(raw_bytes))
    known_face_encodings=face_recognition.face_encodings(known_image)
    return known_face_encodings