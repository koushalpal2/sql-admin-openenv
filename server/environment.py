import sqlite3
from models import SQLAction, SQLObservation, SQLState
from openenv.core.env_server import Environment

# We MUST inherit from the official OpenEnv Environment class!
class SQLEnvironment(Environment[SQLAction, SQLObservation, SQLState]):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.cursor = None
        self.current_task = 1
        self.step_count = 0
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

    def reset(self, seed=None, episode_id=None, **kwargs) -> SQLObservation:
        self._setup_database()
        self.current_task = 1
        self.step_count = 0
        intro = "Connected to DB. Task 1: We lost Charlie's email. Write a query to find it."
        
        # Explicitly pass error=None to satisfy the strict Python initialization!
        return SQLObservation(result=intro, error=None, reward=0.0, done=False)

    def step(self, action: SQLAction, timeout_s=None, **kwargs) -> SQLObservation:
        self.step_count += 1
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

        reward, done, obs_result = self._grade_task(obs_result)
        
        return SQLObservation(result=obs_result, error=obs_error, reward=float(reward), done=bool(done))

    def _grade_task(self, obs_result: str):
        reward = 0.0
        done = False

        if self.current_task == 1:
            if obs_result and "charlie@hidden.com" in obs_result:
                reward = 1.0
                self.current_task = 2
                obs_result += "\n\n[SYSTEM] Task 1 Complete! Task 2: Change user ID 45 status to 'active'."
                
        elif self.current_task == 2:
            self.cursor.execute("SELECT status FROM users WHERE id=45")
            status = self.cursor.fetchone()
            if status and status[0] == 'active':
                reward = 1.0
                self.current_task = 3
                obs_result += "\n\n[SYSTEM] Task 2 Complete! Task 3: Delete all orders belonging to users with a 'deleted' status."

        elif self.current_task == 3:
            self.cursor.execute("SELECT COUNT(*) FROM orders JOIN users ON orders.user_id = users.id WHERE users.status = 'deleted'")
            bad_orders = self.cursor.fetchone()
            bad_orders = bad_orders[0] if bad_orders else 0
            
            self.cursor.execute("SELECT COUNT(*) FROM orders")
            total_orders = self.cursor.fetchone()
            total_orders = total_orders[0] if total_orders else 0
            
            if bad_orders == 0 and total_orders > 0:
                reward = 1.0
                done = True
                obs_result += "\n\n[SYSTEM] Task 3 Complete! You are a master Database Admin!"

        return reward, done, obs_result

    @property
    def state(self) -> SQLState:
        return SQLState(current_task=self.current_task, step_count=self.step_count)
