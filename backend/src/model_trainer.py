import replicate
from config import Config
import os

class ModelTrainer:
    def __init__(self, model_name, trigger_word):
        self.model_name = model_name
        self.trigger_word = trigger_word
        os.environ["REPLICATE_API_TOKEN"] = Config.REPLICATE_API_TOKEN

    def create_model(self, visibility="private"):
        return replicate.models.create(
            owner="a-turcu",
            name=self.model_name,
            visibility=visibility,
            hardware="gpu-a40-small" # will be overwritten to a h100 for finetune
        )

    def train_model(self, input_images_path):
        training = replicate.trainings.create(
            destination=f"a-turcu/{self.model_name}",
            # how to get the latest version?
            version="ostris/flux-dev-lora-trainer:latest",
            input={
                "steps": 1800,
                "lora_rank": 16,
                "optimizer": "adamw8bit",
                "batch_size": 1,
                "resolution": "1024",
                "autocaption": False,
                "input_images": open(input_images_path, "rb"),
                "trigger_word": self.trigger_word,
                "learning_rate": 0.0004,
                # only keep wandb for testing purposes
                "wandb_api_key": Config.WANDB_API_KEY,
                "wandb_sample_prompts": self.trigger_word,
                "wandb_project": f"flux-{self.model_name}",
                "wandb_run": "default"
            },
        )
        return training