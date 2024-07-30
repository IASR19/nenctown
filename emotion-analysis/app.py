import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from deepface import DeepFace

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

emotion_translation = {
    'angry': 'Raiva',
    'disgust': 'Desgosto',
    'fear': 'Medo',
    'happy': 'Felicidade',
    'sad': 'Tristeza',
    'surprise': 'Surpresa',
    'neutral': 'Neutro'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(directory, filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}({counter}){extension}"
        counter += 1
    return new_filename

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = get_unique_filename(app.config['UPLOAD_FOLDER'], filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        return jsonify(filename=unique_filename)
    return jsonify(error='File not allowed'), 400

@app.route('/analyze/<filename>', methods=['GET'])
def analyze_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify(error='File not found'), 404
    try:
        analysis = DeepFace.analyze(img_path=filepath, actions=['emotion'])
        emotion = analysis[0]['dominant_emotion']
        emotion_pt = emotion_translation.get(emotion, emotion)
        return jsonify(emotion=emotion_pt)
    except Exception as e:
        os.remove(filepath)  # Exclui o arquivo se ocorrer um erro
        return jsonify(error=str(e)), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/analyze-all', methods=['GET'])
def analyze_all_files():
    emotions_count = {emotion: 0 for emotion in emotion_translation.values()}
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                analysis = DeepFace.analyze(img_path=filepath, actions=['emotion'])
                emotion = analysis[0]['dominant_emotion']
                emotion_pt = emotion_translation.get(emotion, emotion)
                emotions_count[emotion_pt] += 1
            except Exception as e:
                os.remove(filepath)  # Exclui o arquivo se ocorrer um erro
    return jsonify(emotions=emotions_count)

if __name__ == '__main__':
    app.run(debug=True)