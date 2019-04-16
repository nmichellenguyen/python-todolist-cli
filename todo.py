import os
import sqlite3
import fire

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "database.sqlite3")


def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con


def db_create():
    con = db_connect()
    sql = """
    CREATE TABLE IF NOT EXISTS todo (
        id INTEGER PRIMARY KEY,
        todo_text text NOT NULL,
        due_date DATE NOT NULL,
        project_id INTEGER NOT NULL,
        status text DEFAULT "incomplete")

    """

    cur = con.cursor()
    cur.execute(sql)
    con.close()


def incomplete_status():
    con = db_connect()
    sql = """
    ALTER TABLE todo
    ADD status text DEFAULT "incomplete";
    """
    cur = con.cursor()
    cur.execute(sql)
    con.close()


def mark_complete(id):
    con = db_connect()
    sql = """
    UPDATE todo
    SET status = 'complete'
    WHERE id = ?;
    """
    cur = con.cursor()
    cur.execute(sql, (id,))
    con.commit()

    con.close()


def list_db(status, project_id, due_date):
    con = db_connect()

    def sort_date(a):
        return {"ASC": "ASC", "DESC": "DESC"}[a]

    x = sort_date(due_date)

    sql = f"""
    SELECT *
    FROM todo 
    WHERE status = ? AND project_id = ?
    ORDER BY due_date {x}
    """
    cur = con.cursor()
    cur.execute(sql, (status, project_id))
    results = cur.fetchall()
    for row in results:
        print(row)

    con.close()


def add_todo(todo_text, due_date, project_id):
    con = db_connect()
    sql = """
    INSERT INTO todo (todo_text, due_date, project_id)
    VALUES (?, ?, ?);
    """

    cur = con.cursor()
    cur.execute(sql, (todo_text, due_date, project_id))
    con.commit()

    select_sql = """
    SELECT * FROM todo;
    """
    cur.execute(select_sql)

    results = cur.fetchall()
    for row in results:
        print(row)

    con.close()
    

def print_table():
    con = db_connect()
    sql = """
    SELECT *
    FROM todo;
    """

    cur = con.cursor()
    cur.execute(sql)
    con.commit()

    select_sql = """
    SELECT * FROM todo;
    """
    cur.execute(select_sql)

    results = cur.fetchall()
    for row in results:
        print(row)

    con.close()

if __name__ == "__main__":
    fire.Fire(
        {
            "add_todo": add_todo,
            "db_create": db_create,
            "incomplete_status": incomplete_status,
            "mark": mark_complete,
            "print_todo": list_db,
            "print_all": print_table,
        }
    )
