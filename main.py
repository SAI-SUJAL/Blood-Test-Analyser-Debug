from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
from agents import doctor, verifier, nutritionist, exercise_specialist
from task import help_patients, nutrition_analysis, exercise_planning, verification
from PyPDF2 import PdfReader
import uvicorn

app = FastAPI(title="Blood Test Report Analyser")

def run_crew(query: str, file_path: str):
    """To run the whole crew"""
    try:
        medical_crew = Crew(
            agents=[verifier,doctor,nutritionist,exercise_specialist],
            tasks=[verification,help_patients,nutrition_analysis,exercise_planning],
            process=Process.sequential,
            verbose=True
        )

        # Use forward slashes for cross-platform compatibility
        normalized_path = file_path.replace("\\", "/")
        
        inputs = {
            'query': query,
            'path': normalized_path
        }
        print('inputs:', inputs)

        result = medical_crew.kickoff(inputs=inputs)
        return result
    
    except Exception as e:
        print(f"Crew execution error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""

    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    from pathlib import Path

    BASE_DIR = Path("C:/Users/91998/Desktop/blood-test-analyser-debug/data")  # Simplified path - no hardcoded Windows path
    BASE_DIR.mkdir(exist_ok=True)  # Create directory if it doesn't exist
    
    unique_filename = f"blood_test_report_{uuid.uuid4()}.pdf"
    file_path = BASE_DIR / unique_filename
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate file was saved
        if not file_path.exists():
            raise HTTPException(status_code=500, detail="Failed to save uploaded file")

        # Validate query
        if not query or query.strip() == "":
            query = "Summarise my Blood Test Report"

        # Process the blood report
        response = run_crew(query=query.strip(), file_path=str(file_path))
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename,
            "file_size": len(content)
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other errors
        print(f"Error processing blood report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")

    finally:
        # Clean up uploaded file
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"Cleaned up file: {file_path}")
            except Exception as cleanup_error:
                print(f"Warning: Could not clean up file {file_path}: {cleanup_error}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)