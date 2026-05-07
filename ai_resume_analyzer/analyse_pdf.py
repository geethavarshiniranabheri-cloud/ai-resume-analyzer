from google import genai
from dotenv import load_dotenv
import os
import time

# Load .env
load_dotenv()

# API Key
api_key = os.getenv("GEMINI_API_KEY")

# Gemini Client
client = genai.Client(api_key=api_key)


def analyze_resume_gemini(
    resume_content,
    job_description
):

    prompt = f"""
    You are an expert ATS Resume Analyzer.

    Analyze the resume based on the job description.

    Resume:
    {resume_content}

    Job Description:
    {job_description}

    Tasks:
    1. Give ATS Match Score out of 100
    2. Mention Missing Skills
    3. Mention Strengths
    4. Give Suggestions
    5. Provide Final Summary
    """

    # Retry logic
    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            print(f"Attempt {attempt+1} failed...")

            time.sleep(10)

    return "Server busy. Please try again later."