import os
from openai import OpenAI
from server.environment import Environment
from models import Action

# 1. Setup the AI Client (Using Hackathon Required Variables)
# For local testing, we will fall back to a fake key if the real ones aren't set yet.
api_key = os.getenv("HF_TOKEN", "fake-local-key")
base_url = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")

client = OpenAI(api_key=api_key, base_url=base_url)

# 2. Boot up the Game Server
env = Environment()
print("--- BOOTING AI PLAYER ---")
obs = env.reset()
print(f"System: {obs.result}\n")

# 3. Ask the AI to solve Task 1
# We give the AI the exact observation from the environment and strict rules.
prompt = f"""
You are an expert SQL Database Administrator. 
The system gives you this task: {obs.result}
Assume the table is named 'users' with columns 'id', 'name', 'email', 'status'.
Reply with ONLY the raw SQL query to solve this. Do not use markdown blocks like ```sql. Do not explain your answer.
"""

print("Thinking...\n")
try:
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract the AI's SQL query
    ai_sql = response.choices[0].message.content.strip()
    print(f"🤖 AI generated this SQL: {ai_sql}")

    # 4. Send the AI's move to the environment
    print("\n--- GRADING AI'S MOVE ---")
    step_result = env.step(Action(sql_query=ai_sql))
    
    print(f"Server Response: {step_result['observation'].result}")
    print(f"Points Awarded: {step_result['reward']}")
    print(f"Is Episode Over?: {step_result['done']}")

except Exception as e:
    print(f"AI Call Failed (Expected if no API key is set yet!): {e}")