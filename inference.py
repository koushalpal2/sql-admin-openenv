import os
from openai import OpenAI
from server.environment import SQLEnvironment
from models import SQLAction

# 1. Setup the AI Client (STRICT COMPLIANCE)
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
# CRITICAL: No fallback allowed for HF_TOKEN per hackathon rules!
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)

def main():
    # 2. Boot up the Game Server
    env = SQLEnvironment()
    
    # REQUIRED LOG: The judge scans for this exact tag to know the game started
    print("[START]") 
    
    obs = env.reset()

    # 3. Ask the AI to solve Task 1
    prompt = f"""
    You are an expert SQL Database Administrator. 
    The system gives you this task: {obs.result}
    Assume the table is named 'users' with columns 'id', 'name', 'email', 'status'.
    Reply with ONLY the raw SQL query to solve this. Do not use markdown blocks like ```sql. Do not explain your answer.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        
        ai_sql = response.choices[0].message.content.strip()

        # REQUIRED LOG: The judge scans for this tag every time the AI makes a move
        print(f"[STEP] AI generated this SQL: {ai_sql}")

        # 4. Send the AI's move to the environment
        step_result = env.step(SQLAction(sql_query=ai_sql))
        
        # Accessing the object properties directly
        print(f"Server Response: {step_result.result}")
        print(f"Points Awarded: {step_result.reward}")
        
        # REQUIRED LOG: The judge scans for this tag to know the run is finished
        print("[END]")

    except Exception as e:
        print(f"AI Call Failed: {e}")
        # Even on failure, we must print [END] so the grader doesn't hang forever
        print("[END]")

if __name__ == "__main__":
    main()
