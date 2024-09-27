from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/upload', methods=['POST'])
def upload_files():
    if 'product_name' not in request.form:
        return jsonify({"error": "No product name provided"}), 400

    product_name = request.form['product_name']
    product_folder = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(product_name))
    
    if not os.path.exists(product_folder):
        os.makedirs(product_folder)

    uploaded_files = request.files.to_dict()
    file_paths = []

    for key, file in uploaded_files.items():
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(product_folder, filename)
            file.save(file_path)
            file_paths.append(file_path)

    if len(file_paths) < 5 or len(file_paths) > 20:
        return jsonify({"error": "Please upload between 5 and 20 images."}), 400

    return jsonify({
        "message": f"Successfully uploaded {len(file_paths)} images for product '{product_name}'",
        "files": file_paths
    }), 200

if __name__ == '__main__':
    app.run(debug=True)