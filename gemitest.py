import os
import google.generativeai as genai
from config import apikey

genai.configure(api_key=apikey)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "write an email to my boss for resignation\n",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Okay, here's a template for a resignation email you can adapt, along with a few options and things to consider...\n",  # Template response
            ],
        },
    ]
)

# Function to generate and save the response
def generate_response_and_save(query):
    response = chat_session.send_message(query)  # Send user input to the model

    # Define the folder and file name
    folder = "responses"
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/response_{len(os.listdir(folder)) + 1}.txt"

    # Save the response text to a file
    with open(filename, 'w') as file:
        file.write(response.text)

    # Return the response text to be used in the main script
    return f"Response saved to {filename}"
