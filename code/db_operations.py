import sqlite3
from credentials_security import Credentials


class DB:
    def __init__(self, db: str):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    # OPERATE WITH USER ACCOUNT
    def create_account(self, email_address, password):
        Credentials.encryptAccount(email=email_address, password=password)
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
        encrypted_email = Credentials.encryptEmail(old_email_address, new_email_address)
        user_emails = [(encrypted_email, old_email_address)]

        self.cursor.executemany('UPDATE user '
                                'SET email=? '
                                'WHERE email=?', user_emails)

        self.conn.commit()

    def update_password(self, email_address, old_password, new_password):
        user_passwords = [(new_password, email_address, old_password)]
        self.cursor.executemany('UPDATE user '
                                'SET password=? '
                                'WHERE email=? and password=?', user_passwords)

        self.conn.commit()

    # DATA RETURN
    def getAllEmails(self, alphabeticalOrder=True, encrypted=True):
        sql_query = 'SELECT email FROM user'
        sql_query_alphabetical_order = 'SELECT email FROM user ORDER BY email'
        for row in self.cursor.execute(sql_query):
            formatted_email = str(row).replace(',', '').replace('(', '').replace(')', '').replace("'", '')
            if alphabeticalOrder:
                for email_row in self.cursor.execute(sql_query_alphabetical_order):
                    formatted_email_row = str(email_row).replace(',', '').replace('(', '').replace(')', '') \
                        .replace("'", '')
                    if encrypted:
                        print(formatted_email_row)
                    else:
                        Credentials.decryptEmail(email=str(formatted_email_row))
            else:
                if encrypted:
                    print(formatted_email)
                else:
                    Credentials.decryptEmail(email=formatted_email)

    def getAllPasswords(self, alphabeticOrder=True, encrypted=True):
        sql_query = 'SELECT password from user'
        sql_query_alphabetical_order = 'SELECT password FROM user ORDER BY email'

        for row in self.cursor.execute(sql_query):
            formatted_password = str(row).replace(',', '').replace('(', '').replace(')', ''.replace("'", ''))
            if alphabeticOrder:
                for password_row in self.cursor.execute(sql_query_alphabetical_order):
                    formatted_password_row = str(password_row).replace(',', '').replace('(', '').replace(')', '') \
                        .replace("'", '')

                    if encrypted:
                        print(formatted_password_row)
                    else:
                        Credentials.decryptPassword(password=str(formatted_password_row))
            else:
                if encrypted:
                    print(formatted_password)
                else:
                    Credentials.decryptPassword(password=str(formatted_password))


if __name__ == "__main__":
    # Instantiate DataBase
    Database = DB('database.db')