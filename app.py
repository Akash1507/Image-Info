from flask import Flask, request, jsonify
import os
from decimal import Decimal
from werkzeug.utils import secure_filename
from PIL import Image


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)

@app.route("/api/upload",methods=['POST'])
def image_upload():
	if request.method == 'POST':
		image_file      = request.files.get('image',None)
		if image_file == None or image_file == "" or image_file == " ":
			return jsonify({"Error":"No Image Uploaded"})

		img_name        = str(secure_filename(image_file.filename))	
		if os.path.exists("./data/"+str(img_name)):
			return jsonify({"Error":"Image file already exists"})

		if image_file and allowed_file(img_name):
			image_file.save("./data/"+str(img_name))
		else:
			return jsonify({"Error":"File Format not supported"})

		img_size = float(round(Decimal((os.path.getsize("./data/"+str(img_name)))/(1024*1024)),2))
		with Image.open("./data/"+str(img_name)) as img:
			width, height = img.size
		return jsonify({"fname":img_name, "fsize":img_size, "fresolution":{"height":height, "width":width}})


		

if __name__=="__main__":
	app.run("0.0.0.0",port=8000)