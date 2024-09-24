from image_generator import ImageGenerator
from model_trainer import ModelTrainer

def main():
    # Image Generation
    generator = ImageGenerator()
    prompt = "TOK aftershave"
    image_urls = generator.generate_images(prompt)
    generator.save_images(image_urls)

    # Model Training
    trainer = ModelTrainer("nivea", "aftershave")
    model = trainer.create_model()
    training = trainer.train_model("nivea/dataset/data.zip")
    print(f"Training started: {training}")

if __name__ == "__main__":
    main()