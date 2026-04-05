# SQL Database Administrator (OpenEnv)

## Environment Description
This environment simulates a real-world task: managing a company's internal SQLite database. The AI agent acts as a Junior Database Administrator and must solve three progressive tasks by sending raw SQL queries to fix data, update user statuses, and execute table joins.

## Action & Observation Spaces
* **Action Space:** A JSON object containing `sql_query` (string).
* **Observation Space:** A JSON object containing `result` (string: the fetched SQL rows or system prompt) and `error` (optional string: captured SQL syntax errors).

## Tasks & Graders
1. **Easy:** Execute a SELECT query to find a specific user's email. (Reward 1.0 if the email string is in the result).
2. **Medium:** Execute an UPDATE query to change a user's status. (Reward 1.0 if the backend database reflects the new status).
3. **Hard:** Execute a JOIN/DELETE query to remove specific corrupted orders. (Reward 1.0 if the backend row count drops to 0 while preserving valid data).

## Setup Instructions
1. Install requirements: `pip install openenv pydantic openai`
2. Define environment variables: `API_BASE_URL`, `MODEL_NAME`, and `HF_TOKEN`.
3. Run the inference script: `python inference.py`