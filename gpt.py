from openai import OpenAI
from utils import log_error

# Initialize the OpenAI client
def gpt_response(prompt, openai_key):
    try:
        client = OpenAI(api_key=openai_key)
        response = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ])
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting response from gpt-4o: {e}")
        log_error(e)
        return "Sorry, I couldn't process that."
