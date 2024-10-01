import os
import random
from PIL import Image
from zipfile import ZipFile
import argparse


# Augmentation parameters
crop_percentage = 0.4  # Amount to crop from the image, e.g., 80%
num_augmentations_per_image = 10  # Number of augmentations to generate per image

def random_crop(img, crop_percentage):
    """Crop the image by a random amount."""
    width, height = img.size
    new_width = int(width * crop_percentage)
    new_height = int(height * crop_percentage)
    left = random.randint(0, width - new_width)
    top = random.randint(0, height - new_height)
    return img.crop((left, top, left + new_width, top + new_height))

def random_flip(img):
    """Randomly flip the image."""
    if random.choice([True, False]):
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    if random.choice([True, False]):
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    return img

def augment_image(img):
    """Apply random augmentations."""
    flips = [random_flip(img) for _ in range(6)]
    crops = [random_crop(img, crop_percentage) for _ in range(8)]
    fl_cr = [random_flip(random_crop(img, crop_percentage)) for _ in range(6)]
    return flips, crops, fl_cr

def save_images(img_list, augm_type):
    for i, img in enumerate(img_list):
        augmented_img_path = os.path.join(image_dir, f'{filename.split(".")[0]}_{augm_type}_{i}.png')
        img.save(augmented_img_path)


def parse_experiment_settings():
    parser = argparse.ArgumentParser(description='Prepare images for REPLICATE training and inference')
    parser.add_argument('-dir', '--dir', type=str, help='Directory containing images to be parsed.', default=os.getcwd(), required=False)
    parser.add_argument('-zip', '--zip_to', help='Path where to save the zip archive', default=os.path.join(os.getcwd(), 'archive'), type=str, required=False)
    parser.add_argument('-t', '--trigger', help='Desired trigger word to use as image captions', type=str, required=False, default='TOK')
    return vars(parser.parse_args())

class FilePreparer:
    def __init__(self, zip_path, image_dir, trigger_word):
        self.image_dir = image_dir
        self.trigger_word = trigger_word
        self.zip_path = zip_path
        self.prepared_files = []
            
    def make_captions(self):
        for filename in os.listdir(self.image_dir):
            if filename.lower().endswith('_cropped.png'):
                # Create a text file with the same name as the image file (but with .txt extension)
                text_filename = f"{os.path.splitext(filename)[0]}.txt"
                text_file_path = os.path.join(self.image_dir, text_filename)
                
                # Write the text "hello" to the text file
                with open(text_file_path, 'w') as file:
                    file.write(self.trigger_word)

        print("Text files created for each image!")

    # Function to resize and center crop an image to 1024x1024
    def resize_and_center_crop(self, img):

        width, height = img.size
        print(f"Original image size: {width}x{height}")

        # Determine the smaller dimension and scale accordingly
        if width > height:
            # Resize height to 1024, maintaining aspect ratio
            new_height = 1024
            new_width = int((1024 / height) * width)
        else:
            # Resize width to 1024, maintaining aspect ratio
            new_width = 1024
            new_height = int((1024 / width) * height)

        # Resize the image
        resized_img = img.resize((new_width, new_height))
        print(f"Resized image size: {new_width}x{new_height}")

        # Calculate center crop dimensions
        left = (new_width - 1024) / 2
        top = (new_height - 1024) / 2
        right = (new_width + 1024) / 2
        bottom = (new_height + 1024) / 2
        print(f"Cropping image to: {left, top, right, bottom}")

        # Perform center crop
        cropped_img = resized_img.crop((left, top, right, bottom))

        return cropped_img

    def make_archive(self):
    # Create object of ZipFile
        with ZipFile(self.zip_path, 'w') as zip_object:
            for file in self.prepared_files:
                zip_object.write(file, os.path.basename(file))
                text_file = file[:-4] + '.txt'
                zip_object.write(text_file, os.path.basename(text_file))

        print(f"Archive created at: {self.zip_path}")

    def parse_images(self):
        for filename in os.listdir(self.image_dir):
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                img_path = os.path.join(self.image_dir, filename)
                img = Image.open(img_path)

                # 1. Crop to 1024x1024
                cropped_img = self.resize_and_center_crop(img)
                crop_path = img_path[:-4]+"_cropped.png"
                cropped_img.save(crop_path)

                # 2. Add to list of processed images
                self.prepared_files.append(crop_path)

            # 3. Add captions with trigger word
            self.make_captions()

            # 4. Create zip file with all images and their captions.
            self.make_archive()