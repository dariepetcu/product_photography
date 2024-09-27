import replicate
import requests
from PIL import Image
from io import BytesIO
import time
from config import Config
import os

class ImageGenerator:
    def __init__(self, model):
        self.model = model
        os.environ["REPLICATE_API_TOKEN"] = Config.REPLICATE_API_TOKEN

    def generate_images(self, prompt, num_outputs=1):
        # TODO: look into async and replicate.prediction
        start_time = time.time()
        output = replicate.run(
            self.model,
            input={
                "model": "dev",
                "prompt": prompt,
                "lora_scale": 1,
                "num_outputs": num_outputs,
                "aspect_ratio": "1:1",
                "output_format": "png",
                "guidance_scale": 3.5,
                "num_inference_steps": 28
            }
        )
        print(f"Execution time: {time.time()-start_time} seconds")
        return output

    def save_images(self, image_urls, save_dir):
        for i, url in enumerate(image_urls):
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image.save(f"{save_dir}image_{i}.png")
        print(f"Saved {len(image_urls)} images to {save_dir}")