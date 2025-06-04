import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_caption(quote, author):
    prompt = f"""
    כתוב פוסט לאינסטגרם על הציטוט הבא מאת {author}:

    "{quote}"

    כלול תיאור קצר, משפט השראה, ו־5 עד 10 האשטגים רלוונטיים בעברית.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
    except Exception as e:
        # fallback to gpt-3.5-turbo
        print(f"⚠️ Falling back to gpt-3.5-turbo: {e}")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )

    return response.choices[0].message.content.strip()
