import gradio as gr
import numpy as np
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

# Load the pretrained processor and model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def caption_image(input_image: np.ndarray):
    """Generates a caption for the given image input."""
    # Convert numpy array to PIL Image and convert to RGB
    raw_image = Image.fromarray(input_image).convert('RGB')

    # Process the image
    # Note: Adding text prefix "the image of" often improves BLIP's descriptive accuracy
    inputs = processor(images=raw_image, text="the image of", return_tensors="pt")

    # Generate a caption for the image
    outputs = model.generate(**inputs, max_length=50)

    # Decode the generated tokens to text
    caption = processor.decode(outputs[0], skip_special_tokens=True)

    return caption


# Create the Gradio interface
iface = gr.Interface(
    fn=caption_image, 
    inputs=gr.Image(type="numpy"), 
    outputs="text", 
    title="Image Captioning App", 
    description="Upload an image to generate a caption using a BLIP model."
)

# Launch the app with parameters for remote accessibility
iface.launch(server_name="0.0.0.0", server_port=7860, share=True)