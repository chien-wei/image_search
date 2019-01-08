from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory
)
from werkzeug.exceptions import abort
from flaskr.db import get_mongo_client
import cv2
import os
from werkzeug.utils import secure_filename

bp = Blueprint('blog', __name__)

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


def norm_hist_64(im):
    """
    :param im: image object
    :return: (1x64 list) 64 dimension histogram from im
    """
    hist = cv2.calcHist([im], [0, 1, 2], None, [4, 4, 4], [0, 256, 0, 256, 0, 256])
    hist = list(map(int, hist.flatten()))
    size = sum(hist)
    hist = [i/size*100 for i in hist]
    return hist

"""
@bp.route('/')
def index():
mp = get_mongo_client()
    print('index', mp)
    res = mp.query([11.164474487304688, 0.05191167195638021, 0.0, 0.0, 2.5472323099772134, 1.4715194702148438,
                    0.00022252400716145834, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.119781494140625,
                    0.0010808308919270833, 0.0, 0.0, 1.7841021219889324, 16.666793823242188, 0.32784144083658856, 0.0,
                    0.0, 1.2158711751302083, 1.6774177551269531, 0.0007947285970052084, 0.0, 0.0, 0.0,
                    0.000031789143880208336, 0.0, 0.0, 0.0, 0.0, 0.0, 0.101470947265625, 0.00006357828776041667, 0.0,
                    0.0, 36.63552602132162, 20.49719492594401, 0.010585784912109375, 0.0, 0.0, 0.9306589762369791,
                    1.5670458475748699, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.021870930989583332, 0.0,
                    0.0, 0.0, 0.055631001790364586, 3.1508763631184897], 10)
    print(res)
    return 'hello'

    return render_template('image_upload.html')
    """

@bp.route('/')
def upload():
    return render_template('image_upload.html')

@bp.route('/result', methods=['POST'])
def uploaded_file():
    filename = request.args.get('filename')
    results = request.args.get('results')
    results = results.split(' ')
    return render_template("result.html", image_name=filename, results=results)

@bp.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        result = request.form

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            img = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))
            features = norm_hist_64(img)
            if len(img) * len(img[0]) > 250000:
                img = cv2.resize(img, (500, 500), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(UPLOAD_FOLDER + '/' + filename, img)

            mp = get_mongo_client()
            results = mp.query(features, 10)
            print(results)
            results = ' '.join(results)

            return redirect(url_for('blog.uploaded_file', filename=filename, results=results), code=307)

        return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
              <input type=file name=file>
              <input type=submit value=Upload>
            </form>
            '''

@bp.route('/gallery')
def get_gallery():
    image_names = os.listdir(UPLOAD_FOLDER)
    for i in range(len(image_names))[::-1]:
        if not allowed_file(image_names[i]):
            image_names.pop(i)
    print(image_names)
    return render_template("gallery.html", image_names=image_names)
    #return image_names


