import sqlite3

class DBHelper:
    def __init__(self, dbname="user_numbers.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname,check_same_thread=False)

    def setup(self):
        statement = "CREATE TABLE IF NOT EXISTS numbers (id_user INTEGER,numb TEXT)"

        self.conn.execute(statement)
        self.conn.commit()

    def drop(self):
        statement = "DROP TABLE numbers"

        self.conn.execute(statement)
        self.conn.commit()

    def add_user_number(self, id_user, number):
        statement = "INSERT INTO numbers VALUES (?,?)"
        args = (id_user, number)
        self.conn.execute(statement, args)
        self.conn.commit()

    def get_user_number(self, id_user):
        statement = "SELECT numb FROM numbers WHERE id_user = ?"
        args = (id_user,)
        return self.conn.execute(statement, args)

    def update_user_number(self, id_user, number):
        statement = "UPDATE numbers SET numb = ? WHERE id_user = ?"
        args = (number, id_user)
        self.conn.execute(statement, args)
        self.conn.commit()
