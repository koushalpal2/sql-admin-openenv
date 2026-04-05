import sqlite3
from models import Action, Observation

class Environment:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.current_task = 1
        self.reset()

    def _setup_database(self):
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, status TEXT)''')
        self.cursor.execute('''CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, item TEXT)''')
        
        self.cursor.execute('''INSERT INTO users VALUES (1, 'Alice', 'alice@email.com', 'active')''')
        self.cursor.execute('''INSERT INTO users VALUES (3, 'Charlie', 'charlie@hidden.com', 'active')''')
        self.cursor.execute('''INSERT INTO users VALUES (45, 'Dave', 'dave@email.com', 'suspended')''')
        self.cursor.execute('''INSERT INTO users VALUES (99, 'Eve', 'eve@email.com', 'deleted')''')
        
        self.cursor.execute('''INSERT INTO orders VALUES (101, 1, 'Laptop')''')
        self.cursor.execute('''INSERT INTO orders VALUES (102, 99, 'Mouse')''')
        self.conn.commit()

    def reset(self):
        self._setup_database()
        self.current_task = 1
        intro = "Connected to DB. Task 1: We lost Charlie's email. Write a query to find it."
        return Observation(result=intro)

    def step(self, action: Action):
        obs_result = ""
        obs_error = None
        
        try:
            self.cursor.execute(action.sql_query)
            rows = self.cursor.fetchall()
            if not rows:
                self.conn.commit()
                obs_result = "Query executed successfully. 0 rows returned."
            else:
                obs_result = str(rows)
        except Exception as e:
            obs_result = "SQL Syntax Error"
            obs_error = str(e)

        obs = Observation(result=obs_result, error=obs_error)
        reward, is_done = self._grade_task(obs)
        
        # Standard tuple return for the FastAPI Grader Bot
        return obs, float(reward), bool(is_done), {}

    def _grade_task(self, obs: Observation):
        reward = 0.0
        done = False

        if self.current_task == 1:
            if obs.result and "charlie@hidden.com" in obs.result:
                reward = 1.0
                self.current_task = 2
                obs.result += "\n\n[SYSTEM] Task 1 Complete! Task 2: Change user ID 45 status to 'active'."
                
        elif self.current_task == 2:
            self.cursor.execute("SELECT status FROM users WHERE id=45")
            status = self.cursor.fetchone()[0]
            if status == 'active':
                reward = 1.0
                self.current_task = 3
                obs.result += "\n\n[SYSTEM] Task 2 Complete! Task 3: Delete all orders belonging to users with a 'deleted' status."

        elif self.current_task == 3:
            self.cursor.execute("SELECT COUNT(*) FROM orders JOIN users ON orders.user_id = users.id WHERE users.status = 'deleted'")
            bad_orders = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM orders")
            total_orders = self.cursor.fetchone()[0]
            
            if bad_orders == 0 and total_orders > 0:
                reward = 1.0
                done = True
                obs.result += "\n\n[SYSTEM] Task 3 Complete! You are a master Database Admin!"

        return reward, done
