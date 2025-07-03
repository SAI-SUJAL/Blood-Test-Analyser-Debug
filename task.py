from crewai import Task
from agents import doctor, verifier, nutritionist, exercise_specialist

help_patients = Task(
    description=(
        "Use the read_blood_report tool to analyze the blood report at path: '{path}'. "
        "For query: '{query}', identify abnormal values and explain in simple terms. "
        "Keep response under 200 words. Focus only on key findings."
    ),
    expected_output=(
        "Brief summary (max 200 words):\n"
        "- 3-5 key abnormal values found\n"
        "- Simple explanation of what each means\n"
        "- Note: 'Consult your doctor for diagnosis'"
    ),
    agent=doctor,
    async_execution=False
)

verification = Task(
    description=(
        "Use the read_blood_report tool to check if file at path: '{path}' is a valid blood test report. "
        "Look for medical test names and numerical values. "
        "Respond in 1-2 sentences only."
    ),
    expected_output=(
        "Single answer: 'Yes - Valid blood report with [test types found]' or 'No - Not a valid blood report'"
    ),
    agent=verifier,
    async_execution=False,
)

nutrition_analysis = Task(
    description=(
        "Use the read_blood_report tool to read file at path: '{path}'. "
        "For query: '{query}', identify nutrition-related deficiencies. "
        "Give only 3-4 specific dietary recommendations. Keep under 150 words."
    ),
    expected_output=(
        "Short nutrition advice (max 150 words):\n"
        "• Deficiency 1: Food recommendation\n"
        "• Deficiency 2: Food recommendation\n"
        "• Deficiency 3: Food recommendation\n"
        "• Optional: One supplement suggestion"
    ),
    agent=nutritionist,
    async_execution=False
)

exercise_planning = Task(
    description=(
        "Use the read_blood_report tool to read file at path: '{path}'. "
        "For query: '{query}', check for exercise safety markers (heart, inflammation). "
        "Give brief exercise plan in under 100 words."
    ),
    expected_output=(
        "Exercise plan (max 100 words):\n"
        "• Safety status: Safe/Caution/Medical clearance needed\n"
        "• Cardio: [specific recommendation]\n"
        "• Strength: [specific recommendation]\n"
        "• Frequency: [days per week]"
    ),
    agent=exercise_specialist,
    async_execution=False
)