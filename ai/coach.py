import os
from google import genai
import streamlit as st

def get_ai_coach_response(prompt: str, language: str = "English") -> str:
    """
    Calls the Gemini API to generate Maya's trading coach response.
    """
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    
    # Initialize client with the API key
    client = genai.Client(api_key=api_key)
    
    system_prompt = (
        f"You are Maya, an expert AI trading coach and financial analyst. "
        f"Your job is to provide sharp, realistic financial insights, analyze market risks, "
        f"evaluate stock tips objectively, and help the user build smart trading discipline. "
        f"You must respond in {language}."
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config={
                'system_instruction': system_prompt,
                'temperature': 0.7,
            }
        )
        return response.text
    except Exception as e:
        return f"Maya's brain is temporarily offline (Error: {str(e)}). Please check your API key configuration."
