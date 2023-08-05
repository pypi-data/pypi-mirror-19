import sqlite3

from tudo.task import Task


class TasksStore:
    def __init__(self, db_name="database.db"):
        self.conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn_cursor = self.conn.cursor()
        self.init()
        TasksStore.active_db = self

    def add_task(self, description):
        self.conn_cursor.execute("""INSERT INTO tasks (description, important, urgent) VALUES(?, ?, ?)""",
                                 [description, 0, 0])
        self.conn.commit()

    def add_task_p(self, values):
        self.conn_cursor.execute("""INSERT INTO tasks (description, important, urgent) VALUES(?, ?, ?)""",
                                 [values[0], int(values[1]), int(values[2])])
        self.conn.commit()

    def list_tasks(self):
        self.conn_cursor.execute("SELECT * FROM tasks")
        # print(str(self.conn_cursor.fetchall()))
        return [Task(task[0], task[1], task[2], task[3], task[4], task[5]) for task in self.conn_cursor.fetchall()]

    def list_tasks_p(self, important, urgent):
        self.conn_cursor.execute("SELECT * FROM tasks WHERE urgent = ? AND important = ?", [urgent, important])
        # print(str(self.conn_cursor.fetchall()))
        return [Task(task[0], task[1], task[2], task[3], task[4], task[5]) for task in self.conn_cursor.fetchall()]

    def group_tasks_archived(self): # FIXME: Localize group date
        self.conn_cursor.execute('''
        SELECT DATE(finished) AS finished_date,
        COUNT(*) AS num_finished
        FROM tasks
        WHERE finished IS NOT NULL
        GROUP BY DATE(finished)
        ORDER BY finished_date
        ''')
        return [[row[0], row[1]] for row in self.conn_cursor.fetchall()]

    def init(self):
        self.conn_cursor.execute("""CREATE TABLE IF NOT EXISTS tasks
                            (number INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, started TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            , finished TIMESTAMP, important INTEGER, urgent INTEGER)""")
        self.conn.commit()

    def remove(self, numbers):
        for number in numbers:
            self.conn_cursor.execute("""DELETE FROM tasks WHERE number=?""", number)
        self.conn.commit()

    def set_done(self, numbers):
        for number in numbers:
            self.conn_cursor.execute("""UPDATE tasks SET finished = CURRENT_TIMESTAMP WHERE number=?""", number)
        self.conn.commit()

    def reset(self):
        self.conn_cursor.execute("""DROP TABLE tasks""")
        self.init()
