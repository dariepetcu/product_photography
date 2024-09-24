import replicate
import requests
from PIL import Image
from io import BytesIO
import time
from config import Config
import os

class ImageGenerator:
    def __init__(self):
        self.model = "a-turcu/varta:8e1d803a9c3b9e7c836fed8bc2a0fc5f1a44665012c7299dd97dc8ec0c8210a5"
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

    def save_images(self, image_urls):
        for i, url in enumerate(image_urls):
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image.save(f"{Config.SAVE_DIR}image_{i}.png")
        print(f"Saved {len(image_urls)} images to {Config.SAVE_DIR}")