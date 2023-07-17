import sqlite3, time
from datetime import timedelta


class Database():
    def __init__(self):
        self.connection = sqlite3.connect("dbase.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def user_exists(self, user_id):
        with self.connection:
            resp = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id, )).fetchone()
        return bool(resp)

    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO users(user_id) VALUES(?)", (user_id, ))

    def get_all_users(self):
        with self.connection:
            return [t[0] for t in self.cursor.execute("SELECT user_id FROM users").fetchall()]

# db = Database()
# print(db.get_all_users())
# db.add_payment(123, "agkgkoAKO=1GAKG1wegamgaogek3-gjd")
# db.add_user(123)
# print(db.has_access(818525681))

