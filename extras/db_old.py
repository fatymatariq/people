import sqlite3

DATABASE_NAME = "people.db"


def get_conn():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_tables():

    create_table_cmds = [
        "DROP TABLE IF EXISTS person;", 
        """ 
            CREATE TABLE person (
                id INTEGER PRIMARY KEY,
                lname VARCHAR UNIQUE,
                fname VARCHAR,
                timestamp DATETIME
            );
        """   
    ]
    with get_conn() as conn:
        cursor = conn.cursor()
        try:
            for cmd in create_table_cmds:
                cursor.execute(cmd)
            conn.commit()
            print("Person table created successfully.")
        except:
            print("Person table creation failed.")

def insert_persons():
    with get_conn() as conn:
        cur = conn.cursor()

        people = [
            "1, 'Fairy', 'Tooth', '2022-10-08 09:15:10'",
            "2, 'Ruprecht', 'Knecht', '2022-10-08 09:15:13'",
            "3, 'Bunny', 'Easter', '2022-10-08 09:15:27'",
        ]
        for person_data in people:
            insert_cmd = f"INSERT INTO person VALUES ({person_data})"
            cur.execute(insert_cmd)
        conn.commit()
        
        cur.execute("SELECT person.id AS person_id, person.lname AS person_lname, person.fname AS person_fname, person.timestamp AS person_timestamp FROM person")
        people = cur.fetchall()
        for person in people:
            print(person)

if __name__ == "__main__":

    create_tables()
    insert_persons()