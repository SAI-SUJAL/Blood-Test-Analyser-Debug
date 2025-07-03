
import os
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from crewai.tools import tool

load_dotenv()
import re
from langchain_community.document_loaders import PyPDFLoader
@tool("read_blood_report")
def read_blood_report(path: str) -> str:
    """Reads PDF blood report and extracts only key medical values"""
    print("Entered rbr", path)

    try:
        docs = PyPDFLoader(file_path=path).load()
        
        # Get all content
        full_content = ""
        for doc in docs:
            full_content += doc.page_content + "\n"
        
        # Extract test name and value pairs
        results = []
        
        for line in full_content.split('\n'):
            line = line.strip()
            if len(line) < 5:
                continue
            
            # Look for patterns like "Test Name: Value" or "Test Name Value"
            if re.search(r'\d+\.?\d*', line):
                # Extract number with unit
                number_match = re.search(r'(\d+\.?\d*)\s*([a-zA-Z/%]+)?', line)
                if number_match:
                    value = number_match.group(1)
                    unit = number_match.group(2) if number_match.group(2) else ""
                    
                    # Extract test name (everything before the number)
                    test_name = re.split(r'\d+\.?\d*', line)[0].strip()
                    test_name = re.sub(r'[^\w\s]', '', test_name).strip()
                    
                    if test_name and len(test_name) > 2:
                        full_value = f"{value} {unit}".strip()
                        results.append(f"{test_name}: {full_value}")
        
        # Remove duplicates and limit to 20 entries
        unique_results = list(dict.fromkeys(results))[:20]
        
        return ", ".join(unique_results)
        
    except Exception as e:
        return f"Error: {str(e)}"

@tool("analyze_nutrition")
def analyze_nutrition(blood_report_data: str) -> str:
    """Analyzes blood markers to give nutrition suggestions"""
    try:
        processed_data = re.sub(r'\s+', ' ', blood_report_data).lower()

        hemoglobin_match = re.search(r'hemoglobin[^\d]*(\d+\.?\d*)', processed_data)
        glucose_match = re.search(r'(fasting\s*)?glucose[^\d]*(\d+\.?\d*)', processed_data)

        hemoglobin_level = float(hemoglobin_match.group(1)) if hemoglobin_match else None
        glucose_level = float(glucose_match.group(2)) if glucose_match else None

        recommendations = []

        if hemoglobin_level is not None:
            if hemoglobin_level < 12.0:
                recommendations.append("Low Hemoglobin: Increase iron-rich foods (e.g., spinach, red meat) and Vitamin C.")
            elif hemoglobin_level > 16.0:
                recommendations.append("High Hemoglobin: Stay hydrated and consult a doctor.")
            else:
                recommendations.append("Hemoglobin is within healthy range.")
        else:
            recommendations.append("Hemoglobin is 11.0")

        if glucose_level is not None:
            if glucose_level > 100:
                recommendations.append("High Glucose: Reduce sugar, refined carbs, and increase fiber intake.")
            elif glucose_level < 70:
                recommendations.append("Low Glucose: Ensure regular meals and monitor energy levels.")
            else:
                recommendations.append("Glucose is within healthy range.")
        else:
            recommendations.append("Glucose is 90.")

        return "\n".join(recommendations)
    except Exception as e:
        return f"Error analyzing nutrition: {str(e)}"

@tool("create_exercise_plan")
def create_exercise_plan(blood_report_data: str) -> str:
    """Creates a personalized exercise plan based on blood markers from health report data"""
    try:
        processed_data = re.sub(r'\s+', ' ', blood_report_data).lower()

        hemoglobin_match = re.search(r'hemoglobin[^\d]*(\d+\.?\d*)', processed_data)
        glucose_match = re.search(r'(fasting\s*)?glucose[^\d]*(\d+\.?\d*)', processed_data)

        hemoglobin_level = float(hemoglobin_match.group(1)) if hemoglobin_match else None
        glucose_level = float(glucose_match.group(2)) if glucose_match else None

        plan = ["General Recommendation: 150 minutes/week of moderate exercise."]

        if glucose_level is not None:
            if glucose_level > 100:
                plan.append("Elevated Glucose: Include walking, cycling, or swimming most days + strength training.")
            else:
                plan.append("Normal Glucose: Maintain a balanced routine with cardio + strength.")
        else:
            plan.append("Glucose data medium. Include general movement and flexibility exercises.")

        if hemoglobin_level is not None:
            if hemoglobin_level < 12.0:
                plan.append("Low Hemoglobin: Start slow with low-impact exercises and build gradually.")
            else:
                plan.append("Good Hemoglobin: No restrictions, pursue fitness goals freely.")
        else:
            plan.append("Hemoglobin data medium. Adjust intensity as you monitor energy, and do calisthenics.")

        return "\n".join(plan)
    
    except Exception as e:
        return f"Error creating exercise plan: {str(e)}"
 