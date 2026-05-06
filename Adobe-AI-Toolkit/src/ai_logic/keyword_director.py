import os
import json
import random
from groq import Groq
from dotenv import load_dotenv

# 1. FOUNDATION: Load the secret keys
load_dotenv()

def get_hroq_client():
    """Dynamically picks one of your 6 API keys to ensure lightning speed."""
    # We choose from keys 10 through 15
    key_index = random.randint(1, 15)
    api_key = os.getenv(f"GROQ_API_KEY_{key_index}")
    return Groq(api_key=api_key)

def analyze_any_content(transcription_text, video_type="educational"):
    # 2. THE PERSONA DICTIONARY (Intelligence Mapping)
    contexts = {
        "educational": "focus on technical terms, definitions, and complex formulas.",
        "entertainment": "focus on names of celebrities, movies, and pop culture references.",
        "news": "focus on names of politicians, countries, and current events.",
        "sports": "focus on names of athletes, teams, and sports terminology.",
        "business": "focus on names of companies, financial terms, and economic concepts.",
        "marketing": "focus on product names, emotional hooks, and call-to-actions.",
        "health": "focus on medical terms, symptoms, and treatment options.",
        "vlog": "focus on names of places, funny moments, and personal stories.",
        "documentary": "focus on dates, historical figures, and cinematic techniques.",
        "gaming": "focus on names of games, gaming terminology, and popular streamers.",
        "other": "focus on any important keywords, names, and concepts that are relevant."
    }

    selected_context = contexts.get(video_type, "focus on high-impact keywords.")
    
    # 3. THE INSTRUCTION BODY
    system_instruction = (
        f"You are a Video Editing Director. {selected_context} "
        "Return ONLY a JSON object with a list 'keywords' containing: "
        "'word', 'category', 'importance_score' (1-10), and 'visual_suggestion'."
    )

    # 4. PROCESSING (Using the HROQ Bank)
    try:
        client = get_hroq_client()
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": transcription_text}
            ],
            model="llama-3.3-70b-versatile", # Switched to 70b for better 'Architect' level reasoning
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e), "status": "failed"}

# 5. TEST THE SYSTEM
if __name__ == "__main__":
    sample_text = "In Paris, the Eiffel Tower is amazing. You should buy our travel guide for only $10."
    print("--- HROQ Intelligence Engine Launching ---")
    
    # Running marketing logic
    result = analyze_any_content(sample_text, video_type="marketing")
    print(json.dumps(result, indent=4))