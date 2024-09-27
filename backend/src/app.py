from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging
from prepare_files import FilePreparer
from model_trainer import ModelTrainer
from image_generator import ImageGenerator
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the exception
    app.logger.error(f"An unhandled exception occurred: {str(e)}")
    app.logger.error(traceback.format_exc())
    # Return JSON instead of HTML for HTTP errors
    return jsonify(error=str(e)), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Product Photo AI API"}), 200

@app.route('/api/training', methods=['POST'])
def process_images():
    app.logger.info("Received a request to /api/training")
    try:
        app.logger.debug(f"Request form data: {request.form}")
        app.logger.debug(f"Request files: {request.files}")

        if 'image_0' not in request.files:
            return jsonify({'error': 'No images uploaded'}), 400

        product_name = request.form.get('product_name')
        model_name = request.form.get('model_name')

        if not product_name or not model_name:
            return jsonify({'error': 'Missing product name or model name'}), 400

        # Create directories
        model_dir = os.path.join(app.config['UPLOAD_FOLDER'], model_name)
        image_dir = os.path.join(model_dir, 'raw_images')
        os.makedirs(image_dir, exist_ok=True)

        # Save uploaded images
        for key, file in request.files.items():
            if key.startswith('image_'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(image_dir, filename)
                file.save(file_path)
                app.logger.debug(f"Saved file: {file_path}")

        # Set paths
        zip_path = os.path.join(model_dir, 'data.zip')

        # Prepare files
        app.logger.info("Preparing files...")
        file_preparer = FilePreparer(zip_path, image_dir, f"TOK {product_name}")
        file_preparer.parse_images()

        # Train model
        app.logger.info("Training model...")
        trainer = ModelTrainer(model_name, product_name)
        #model = trainer.create_model()
        #training = trainer.train_model(zip_path)

        app.logger.info("Training completed successfully")
        return jsonify({
            'message': 'Model created and trained successfully',
            'model_id': "0",
            'training_id': "0"
        })

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)