from google import genai


class GeminiClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate(
        self,
        model: str,
        prompt: str,
        **kwargs,
    ):
        return self.client.models.generate_content(
            model=model,
            contents=prompt,
            **kwargs,
        )
