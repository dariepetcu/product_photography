import replicate
from config import Config
import os

class ModelManager:
    def __init__(self, model_name, trigger_word):
        self.model_name = model_name
        self.trigger_word = trigger_word
        os.environ["REPLICATE_API_TOKEN"] = Config.REPLICATE_API_TOKEN
        self.training = None

    # TODO how to check for existing model?
    def create_model(self, visibility="private"):
        # create model only if it doesn't exist

        # not working properly
        try:
            model = replicate.models.get(name=self.model_name)
            return
        except:
            replicate.models.create(
            owner="a-turcu",
            name=self.model_name,
            visibility=visibility,
            hardware="gpu-a40-small" # will be overwritten to a h100 for finetune
            )

    def train_model(self, input_images_path):
        self.training = replicate.trainings.create(
            destination=f"a-turcu/{self.model_name}",
            # how to get the latest version?
            version="ostris/flux-dev-lora-trainer:6f1e7ae9f285cfae6e12f8c18618418cfefe24b07172a17ff10a64fb23a6b772",
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
                #"wandb_api_key": Config.WANDB_API_KEY,
                #"wandb_sample_prompts": self.trigger_word,
                #"wandb_project": f"flux-{self.model_name}",
                #"wandb_run": "default"
            },
        )
    
    def get_training_status(self):
        if self.training is None:
            return "No training started"
        return self.training.status