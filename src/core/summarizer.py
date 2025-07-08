import os
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that summarizes YouTube video titles into short, catchy trend summaries for a newsletter."
                },
                {
                    "role": "user",
                    "content": f"Summarize this YouTube video title in 1 short sentence:\n{text}"
                }
            ],
            max_tokens=50,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return "Summary unavailable."
