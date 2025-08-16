from google import genai
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GeminiAPI():
    """
    A class to create and manage interactions with the Google Gemini API.
    NOTE: In this implementation, this class is only used to quickly instantiate a client.
    """

    def __init__(self, gemini_model: str = ""):
        """
        Initialise a Gemini API client.

        Args:
            gemini_model (str): The model to use for the Gemini API. If this is not provided, the default model will be used.
        """
        self.llm_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash") if not gemini_model else gemini_model

        if not self.llm_api_key:
            raise ValueError("LLM API key is required.")
        
        # Configure the Gemini client
        self.llm = genai.Client(api_key=self.llm_api_key)

    def generate_content(self, prompt: str, image_bytes: bytes | None = None) -> genai.types.GenerateContentResponse:
        """
        Generate content using the Gemini API.

        Args:
            prompt (str): The text prompt to generate content for.
            image_bytes (bytes | None): Optional image bytes to include in the request.
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        # If no image is provided, only take in text input
        if not image_bytes:
            response = self.llm.models.generate_content(model=self.gemini_model, contents=prompt)
        else:
            response = self.llm.models.generate_content(
                model = self.gemini_model,
                contents = [
                genai.types.Part.from_bytes(
                    data=image_bytes,
                    mime_type='image/png',
                ),
                prompt
                ])

        return response
