import openai
from config import OPENAI_API_KEY

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

def get_gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
