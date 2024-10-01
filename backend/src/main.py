from image_generator import ImageGenerator
from backend.src.model_manager import ModelManager
from prepare_files import FilePreparer

def main():
    
    model_name = "nivea"
    product_name = "aftershave"

    # Define paths and trigger word    
    zip_path = f"{model_name}/dataset/data.zip"
    image_dir = f"{model_name}/dataset/raw_images"
    trigger_word = f"TOK {product_name}"
    
    # Generate archive in zip_path
    file_preparer = FilePreparer(zip_path, image_dir, trigger_word)
    file_preparer.parse_images()

    # Model Training
    trainer = ModelManager(model_name, product_name)
    model = trainer.create_model()
    training = trainer.train_model(zip_path)
    print(f"Training started: {training}")


    # Image Generation
    model = "a-turcu/varta:8e1d803a9c3b9e7c836fed8bc2a0fc5f1a44665012c7299dd97dc8ec0c8210a5"
    save_dir = f"{model_name}/generated_images"
    generator = ImageGenerator(model)
    prompt = trigger_word
    # TODO automate prompt generation
    # prompt = PromptGenerator.generate_prompt(description)
    image_urls = generator.generate_images(prompt)
    generator.save_images(image_urls, save_dir)

if __name__ == "__main__":
    main()