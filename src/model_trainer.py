import replicate
from config import Config
import os

class ModelTrainer:
    def __init__(self, model_name, product_name):
        self.model_name = model_name
        self.product_name = product_name
        os.environ["REPLICATE_API_TOKEN"] = Config.REPLICATE_API_TOKEN

    def create_model(self):
        return replicate.models.create(
            owner="a-turcu",
            name=self.model_name,
            visibility="private",
            hardware="gpu-a40-small" # will be overwritten to a h100 for finetune
        )

    def train_model(self, input_images_path):
        training = replicate.trainings.create(
            destination=f"a-turcu/{self.model_name}",
            # how to get the latest version?
            version="ostris/flux-dev-lora-trainer:885394e6a31c6f349dd4f9e6e7ffbabd8d9840ab2559ab78aed6b2451ab2cfef",
            input={
                "steps": 2000,
                "lora_rank": 16,
                "optimizer": "adamw8bit",
                "batch_size": 1,
                "resolution": "1024",
                "autocaption": False,
                "input_images": open(input_images_path, "rb"),
                "trigger_word": f"TOK {self.product_name}",
                "learning_rate": 0.0004,
                # only keep wandb for testing purposes
                "wandb_api_key": Config.WANDB_API_KEY,
                "wandb_sample_prompts": f"TOK {self.product_name}",
                "wandb_project": "flux-nivea",
                "wandb_run": "20picsaugment"
            },
        )
        return training