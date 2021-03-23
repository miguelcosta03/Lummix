import sqlite3
from credentials_security import Credentials


class DB:
    def __init__(self, db: str):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    # OPERATE WITH USER ACCOUNT
    def create_account(self, email_address, password, username):
        credentials = [(email_address, password, username)]
        self.cursor.executemany('INSERT INTO user '
                                'VALUES (?,?, ?)', credentials)
        self.conn.commit()

    def login_account(self, username, password):
        self.cursor.execute("SELECT username, password FROM user "
                            "WHERE username LIKE'" + username + "' AND password LIKE'" + password + "'")
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
        credentials = [(new_password, email_address, old_password)]
        self.cursor.executemany('UPDATE user '
                                'SET password=? '
                                'WHERE email=? AND password=?', credentials)

        self.conn.commit()

    def update_username(self, email_adress, old_username, new_username):
        credentials = [(new_username, email_adress, old_username)]

        self.cursor.executemany('UPDATE user '
                                'SET username=? '
                                'WHERE email=? AND password=?', credentials)
        self.conn.commit()

    def addWebsiteURL(self, username, websiteURL):
        credentials = [(websiteURL, username,)]

        self.cursor.executemany('UPDATE user '
                                'SET websiteURL=? '
                                'WHERE username=?', credentials)

        self.conn.commit()

    def addWebsiteServerHostIP(self, username, hostIP):
        credentials = [(hostIP, username)]

        self.cursor.executemany('UPDATE user '
                                'SET websiteHostServerIP=? '
                                'WHERE username=?', credentials)

    # DATA RETURN
    def getUsername(self, email):
        sql_query = self.cursor.execute('SELECT username FROM user '
                                        'WHERE email=?', email)
        return sql_query

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
                        Credentials.decryptEmail(encrypted_email=str(formatted_email_row))
            else:
                if encrypted:
                    print(formatted_email)
                else:
                    Credentials.decryptEmail(encrypted_email=formatted_email)

    def getAllPasswords(self, alphabeticOrder=True, encrypted=True):
        sql_query = 'SELECT password FROM user'
        sql_query_alphabetical_order = 'SELECT password FROM user ORDER BY password'

        for row in self.cursor.execute(sql_query):
            formatted_password = str(row).replace(',', '').replace('(', '').replace(')', '').replace("'", '')
            if alphabeticOrder:
                for password_row in self.cursor.execute(sql_query_alphabetical_order):
                    formatted_password_row = str(password_row).replace(',', '').replace('(', '').replace(')', '') \
                        .replace("'", '')
                    if encrypted:
                        print(formatted_password_row)
                    else:
                        Credentials.decryptPassword(encrypted_password=str(formatted_password_row))
            else:
                if encrypted:
                    print(formatted_password)
                else:
                    Credentials.decryptPassword(encrypted_password=str(formatted_password))

    def getAllUserNames(self, alphabeticalOrder=True, encrypted=True):
        sql_query = 'SELECT username FROM user'
        sql_query_alphabetical_order = 'SELECT username FROM user ORDER BY username'

        for row in self.cursor.execute(sql_query):
            formatted_username = str(row).replace(',', '').replace('(', '').replace(')', '').replace("'", '')
            if alphabeticalOrder:
                for username_row in self.cursor.execute(sql_query_alphabetical_order):
                    formatted_username_row = str(username_row).replace(',', '').replace('(', '').replace(')', '') \
                        .replace("'", '')
                    if encrypted:
                        print(formatted_username_row)
                    else:
                        Credentials.decryptUserName(encrypted_username=str(formatted_username_row))
            else:
                if encrypted:
                    print(formatted_username)
                else:
                    Credentials.decryptUserName(encrypted_username=formatted_username)

    def getAllWebsiteURLs(self, alphabeticalOrder=True, encrypted=True):
        sql_query = 'SELECT websiteURL FROM user '
        sql_query_alphabetical_order = 'SELECT websiteURL FROM user ORDER BY websiteURL'

        for row in self.cursor.execute(sql_query):
            formatted_websiteURL = str(row).replace(',', '').replace('(', '').replace(')', '').replace("'", '')
            if alphabeticalOrder:
                for websiteURL_row in self.cursor.execute(sql_query_alphabetical_order):
                    formatted_websiteURL_row = str(websiteURL_row).replace(',', '').replace('(', '').replace(')', '')\
                        .replace("'", '')
                    if encrypted:
                        print(formatted_websiteURL_row)
                    else:
                        Credentials.decryptWebsiteURL(encryptedURL=str(formatted_websiteURL_row))
            else:
                if encrypted:
                    print(formatted_websiteURL)
                else:
                    Credentials.decryptWebsiteURL(encryptedURL=str(formatted_websiteURL))

    def getAllHostServerIPs(self, alphabeticalOrder=True, encrypted=True):
        sql_query = 'SELECT websiteHostServerIP FROM user '
        sql_query_alphabetical_order = 'SELECT websiteHostServerIP FROM user ORDER BY websiteHostServerIP'

        for row in self.cursor.execute(sql_query):
            formatted_hostServerIP = str(row).replace(',', '').replace('(', '').replace(')', '').replace("'", '')
            if alphabeticalOrder:
                for hostServerIP_row in self.cursor.execute(sql_query_alphabetical_order):
                    formatted_hostServerIP_row = str(hostServerIP_row).replace(',', '').replace('(', '')\
                        .replace(')', '').replace("'", '')
                    if encrypted:
                        print(formatted_hostServerIP_row)

                    else:
                        Credentials.decryptWebsiteHostServerIP(encryptedIP=str(formatted_hostServerIP_row))
            else:
                if encrypted:
                    print(formatted_hostServerIP)
                else:
                    Credentials.decryptWebsiteHostServerIP(encryptedIP=str(formatted_hostServerIP))



if __name__ == "__main__":
    # Instantiate DataBase For Test Operations Here
    Database = DB('database.db')
