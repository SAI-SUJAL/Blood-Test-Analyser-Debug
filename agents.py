## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()
from crewai import Agent , LLM
from tools import analyze_nutrition, read_blood_report,create_exercise_plan
from crewai import LLM

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key="your api key here",
    temperature=0.4,
    max_tokens=2000
)


doctor = Agent(
    role="Medical Report Analyst",
    goal="Use read_blood_report tool to extract key abnormal values and explain them simply in under 50 words.",
    verbose=True,
    memory=False,  # Disable memory to reduce token usage
    backstory=(
        "Lab report expert. Always use read_blood_report tool first to get blood data. "
        "Focus only on abnormal values. Explain in simple terms. Keep responses short."
    ),
    llm=llm,
    tools=[read_blood_report],
    max_iter=2,  # Reduced iterations
    max_rpm=30,
    allow_delegation=False
)

verifier = Agent(
    role="Lab Report Verifier",
    goal="Use read_blood_report tool to check if document contains valid blood test data. Answer in 1-2 sentences.",
    verbose=True,
    memory=False,
    backstory=(
        "Document validator. Always use read_blood_report tool to check file content. "
        "Look for medical test names and numbers. Give yes/no answer with brief reason."
    ),
    llm=llm,
    tools=[read_blood_report],
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

nutritionist = Agent(
    role="Clinical Nutritionist", 
    goal="Use read_blood_report tool to find nutrition deficiencies and use analyze_nutrition tool to give 3-4 food recommendations in under 50 words.",
    verbose=True,
    memory=False,
    backstory=(
        "Nutrition expert. Always use read_blood_report tool first to get blood values. "
        "Focus on vitamin/mineral deficiencies. Give specific foods, not general advice. Keep it brief."
    ),
    llm=llm,
    tools=[read_blood_report, analyze_nutrition],
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

exercise_specialist = Agent(
    role="Exercise Physiologist",
    goal="Use read_blood_report tool to check exercise safety markers and use create_exercise_plan tool to create brief workout plan in under 50 words.",
    verbose=True,
    memory=False,
    backstory=(
        "Exercise safety expert. Always use read_blood_report tool to check heart/inflammation markers. "
        "Give specific exercise types and frequency. Flag any safety concerns first."
    ),
    llm=llm,
    tools=[read_blood_report, create_exercise_plan],
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)