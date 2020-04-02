## Standard library imports
import base64
import sys
import os

## Append to path
folder_path = os.path.dirname(os.path.abspath(__file__))
SPADE_folder_path = os.path.join(folder_path, "..", "..", "SPADE")
sys.path.append(SPADE_folder_path)

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'HTML'))
sys.path.append(os.path.join(os.getcwd(), 'CNN'))

## Random Imports
import flask
from flask import render_template
import numpy as np
from PIL import Image
import cv2

## Inner-project Imports
from app import app
from generate import *
import extract

# Comment the below line out and insert wherever needed
# visual_features = extract.get_visual_features(generated_img)

g = GAUGAN()
rgb2bw, bw2rgb, classes, class2rgb = load_cmap(os.path.join(SPADE_folder_path, "ade20k_cmap.txt"))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', classes=classes, class2rgb=class2rgb)

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    sent_data = flask.request.args.get('img')
    encoded_data = sent_data.split(',')[1]
    decoded_data = base64.b64decode(encoded_data)
    import io
    img = Image.open(io.BytesIO(decoded_data))
    # Shape (256, 256, 4) in RGBA
    img = np.asarray(img)[:,:,0:3].astype(np.uint8)
    seg_map = convert_drawing_to_segmentation_map(img, rgb2bw)
    seg_map = create_seg_map_tensor(seg_map)
    generated_img = g.generate_from_seg_map(seg_map)
    generated_img = generated_to_savable_image(generated_img)
    save_image(generated_img, os.path.join(folder_path, "test.png"))
    success, return_img = cv2.imencode(".png", generated_img)
    return_img = return_img.tobytes()
    return flask.jsonify({"img":str(base64.b64encode(return_img))})