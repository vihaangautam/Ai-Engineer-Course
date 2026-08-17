import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

JD = "TechFlow Solutions SDE-1 role requiring 1-3 years exp, JavaScript (React/Node.js), Python (FastAPI/Django), PostgreSQL, AWS, Docker, CI/CD, testing"
RESUME = """
Rahul Sharma, 1.5 years exp at InnovateTech:
SDE-1: 5+ FastAPI microservices, React dashboards, 75% latency reduction, CI/CD on AWS ECS
Intern: Django/React admin panel, Python data pipelines (50K records/day)
Projects: Full-stack e-commerce (Next.js/FastAPI/AWS), real-time chat (Socket.io), open-source contributions
Education: B.Tech CSE PES University (8.7 CGPA)
Certs: AWS Cloud Practitioner, Meta Frontend Cert
Achievements: SIH winner, Google Kick Start top 5%, CodeChef 3-star
"""

def ask_llm(system_prompt: str, user_prompt: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content

def step1_res_extract() -> str:
    system_prompt = "You are a professional HR assistant. Extract skills of the candidate from the resume provided. Do not invent skills."
    user_prompt = f"Extract skills from:\n{RESUME}"
    return ask_llm(system_prompt, user_prompt)

def step2_jd_extract() -> str:
    system_prompt = "You are a professional HR assistant. Extract skills from the JD provided. Do not invent skills."
    user_prompt = f"Extract skills from:\n{JD}"
    return ask_llm(system_prompt, user_prompt)

def step3_match(candidate_skills: str, jd_skills: str) -> str:
    system_prompt = "You are a professional HR assistant. Compare the candidate skills against the JD requirements, score out of 100, and provide a verdict on candidate fit."
    user_prompt = f"Candidate Skills:\n{candidate_skills}\n\nJob Description Requirements:\n{jd_skills}"
    return ask_llm(system_prompt, user_prompt)

if __name__ == "__main__":
    cand_skills = step1_res_extract()
    req_skills = step2_jd_extract()
    result = step3_match(cand_skills, req_skills)
    print(result)