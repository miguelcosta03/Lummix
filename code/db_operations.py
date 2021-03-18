import sqlite3
from credentials_security import Credentials


class DB:
    def __init__(self, db: str):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def create_account(self, email_address, password):
        credentials = [(email_address, password)]

        self.cursor.executemany('INSERT INTO user '
                                'VALUES (?,?)', credentials)

        self.conn.commit()

    def delete_account(self, email_adress):
        self.cursor.execute("SELECT rowid, * FROM user")
        rows = self.cursor.fetchall()
        for row in rows:
            if row[1].lower() == email_adress:
                account_id = [row[0]]
                self.cursor.execute('DELETE FROM user '
                                    'WHERE rowid=? ', account_id)
                self.conn.commit()

    def update_email(self, old_email_address, new_email_address):
        user_emails = [(new_email_address, old_email_address)]

        self.cursor.executemany('UPDATE user '
                                'SET email=? '
                                'WHERE email=?', user_emails)

        self.conn.commit()

    @staticmethod
    def encrypt_password(password):
        Credentials.encrypt(password)

    def update_password(self, old_password, new_password):
        encrypted_password = Credentials.encrypt(new_password)
        user_passwords = [(encrypted_password, old_password)]

        self.cursor.executemany('UPDATE user '
                                'SET password=? '
                                'WHERE password=?', user_passwords)

        self.conn.commit()


if __name__ == "__main__":
    # Instantiate DataBase
    Database = DB('database.db')