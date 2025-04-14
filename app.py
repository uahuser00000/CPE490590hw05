# app.py
from flask import Flask, render_template, request, jsonify, session, send_from_directory, url_for
import onnxruntime as ort
import numpy as np
import json
import os

from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "n/a" # i added this for the session import

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Load the ONNX model
ort_session = ort.InferenceSession("mnist_cnn.onnx")


def predict(x):
    """Make prediction using the ONNX model"""
    # Scale the input features
    #scaled_features = scale_features(features)

    # Prepare input for ONNX runtime
    ort_inputs = ort_session.get_inputs()[0].name
    
    # Run inference
    ort_outputs = ort_session.run(None, {ort_inputs: x})
    
    # Get predicted class
    predicted_class = np.argmax(ort_outputs[0], axis=1)[0]
    
    # Get probability scores
    scores = ort_outputs[0][0]
    softmax_scores = np.exp(scores) / np.sum(np.exp(scores))
    
    return {
        "class_id": int(predicted_class),
        "probabilities": {str(i): float(score) for i, score in enumerate(softmax_scores)}
    }

def process_img(filepath):
    img = Image.open(filepath)
    x = img.convert('L')
    x = x.resize((28,28))
    x = np.array(x).astype(np.float32) / 255.0
    x = x.reshape(1, 1,28,28)
    return x


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    example_files = os.listdir(os.path.join('static', 'example'))
    return render_template('index.html', example_files=example_files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/predict', methods=['POST'])
def make_pred ():
    action = request.form.get('action')
    if action == 'upload':
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected.'}), 400

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                procc_img = process_img(filepath)
                result = predict(procc_img)
                session['data'] = {'filepath': filepath, 'filename': filename}
                print(url_for('uploaded_file', filename=filename)) 
                return jsonify({
                    'message': 'Image uploaded and processed.',
                    'image_path':  url_for('uploaded_file', filename=filename),
                    'prediction': result["class_id"],
                    'probabilities': result["probabilities"]
                })
            except Exception as e:
                return jsonify({'error': f'Error processing image: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Invalid file type.'}), 400
    elif action == 'predict':
        data = session.get('data')
        if not data or not os.path.exists(data['filepath']):
            return jsonify({'error': 'No image available to predict.'}), 400
        try:
            x = process_img(data['filepath'])
            result = predict(x)
            return jsonify({
                'message': 'Prediction completed.',
                'image_path': url_for('uploaded_file', filename=data['filename']),
                'prediction': result["class_id"],
                'probabilities': result["probabilities"]
            })
        except Exception as e:
            return jsonify({'error': f'Error during prediction: {str(e)}'}), 500

    elif action == 'example':
        example_image = request.form.get('data-example')
        filepath = os.path.join('static', 'example', example_image)
        try: 
            x = process_img(filepath)
            result = predict(x)
            return jsonify({
                    'message': 'Example predicted.',
                'image_path': url_for('static', 
                    filename=f'example/{example_image}'),
                    'prediction': result["class_id"],
                    'probabilities': result["probabilities"]
                })
        except Exception as e:
                return jsonify({'error': f'Error during example prediction: {str(e)}'}), 500

    else:
        return jsonify({'error': 'No input.'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)