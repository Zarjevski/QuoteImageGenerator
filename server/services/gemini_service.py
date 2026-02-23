import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_caption(quote, author):
    """
    Generate an Instagram post caption for a quote using Google Gemini.
    
    Args:
        quote: The quote text
        author: The author/thinker name
    
    Returns:
        str: Generated Instagram caption in Hebrew
    """
    prompt = f"""
    כתוב פוסט לאינסטגרם על הציטוט הבא מאת {author}:

    "{quote}"

    כלול תיאור קצר, משפט השראה, ו־5 עד 10 האשטגים רלוונטיים בעברית.
    """
    
    try:
        # Use Gemini Pro model
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 300,
            }
        )
        
        return response.text.strip()
    
    except Exception as e:
        print(f"⚠️ Error generating caption with Gemini: {e}")
        # Return a fallback caption if Gemini fails
        return f"""✨ {quote}

— {author}

#פילוסופיה #השראה #ציטוטים #סטואיקיזם"""
