import sqlite3

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise
import hashlib
import os
import secrets
from base64 import b64encode, b64decode


class SQLDatabase():
    '''
        Our SQL database

    '''

    # Get the database running
    def __init__(self, database_args):
        self.conn = sqlite3.connect(database_args)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    # -----------------------------------------------------------------------------

    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.execute("DROP TABLE IF EXISTS relations")
        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE ,
            password TEXT NOT NULL ,
            salt TEXT NOT NULL ,
            publickey TEXT ,
            is_admin INTEGER DEFAULT 0
        )""")

        self.commit()
        # Create the friends_list table
        self.execute("""CREATE TABLE relations(
            user_Id INTEGER REFERENCES  Users(Id),
            friend_Id INTEGER REFERENCES Users(Id),
            message_sending TEXT,
            PRIMARY KEY (user_Id, friend_Id)
        )""")

        self.commit()

        # Add our admin user

        # self.add_user('admin', admin_password, admin=1)

    # -----------------------------------------------------------------------------
    # User handling
    # -----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, publickey, admin=0):

        salt_value = os.urandom(32)
        h_256 = hashlib.new('sha256')

        password = password.encode() + salt_value
        h_256.update(password)
        hashed_pwd = h_256.hexdigest()
        salt = b64encode(salt_value).decode('utf-8')

        sql_cmd = """
                INSERT INTO Users(username, password, salt, publickey ,is_admin)
                VALUES('{username}', '{password}', '{salt}', '{publickey}',{is_admin})
            """
        sql_cmd = sql_cmd.format(username=username, password=hashed_pwd, salt=salt, publickey=publickey, is_admin=admin)

        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------

    # Create friend relations
    def get_userId_by_name(self, username):
        sql_query = """
                SELECT Id
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        ret = self.cur.fetchone()
        if ret:
            return ret[0]
        else:
            return None

    def get_username_by_Id(self, user_id):
        sql_query = """
                SELECT username
                FROM Users
                WHERE Id = '{user_Id}'
            """

        sql_query = sql_query.format(user_Id=user_id)
        self.execute(sql_query)
        ret = self.cur.fetchone()
        if ret:
            return ret[0]
        else:
            return None

    def add_relations(self, username, friend_name):
        user_id = self.get_userId_by_name(username)
        if user_id is None:
            print(11)
            return
        friend_id = self.get_userId_by_name(friend_name)
        if friend_id is None:
            print(22)
            return
        print(user_id)
        print(friend_id)
        sql_cmd = """
                INSERT INTO relations(user_Id,friend_Id,message_sending)
                VALUES({user_Id}, {friend_Id},null)
            """
        sql_cmd1 = sql_cmd.format(user_Id=user_id, friend_Id=friend_id)
        self.execute(sql_cmd1)
        sql_cmd2 = sql_cmd.format(user_Id=friend_id, friend_Id=user_id)
        self.execute(sql_cmd2)
        self.commit()

    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                   SELECT salt
                   FROM Users
                   WHERE username = '{username}' 
               """

        sql_query = sql_query.format(username=username)

        self.execute(sql_query)

        # If our query returns
        salt = self.cur.fetchone()
        if salt is None:
            return False
        b_salt = b64decode(salt[0].encode('utf-8'))
        h_256 = hashlib.new('sha256')
        password = password.encode() + b_salt
        h_256.update(password)
        password_hashed = h_256.hexdigest()
        print("salt：", b_salt)
        print("pass hashed", password_hashed)

        sql_query = """
                SELECT * 
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """

        sql_query = sql_query.format(username=username, password=password_hashed)

        self.execute(sql_query)

        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False

    # List friends
    def get_friend_list(self, username):
        user_id = self.get_userId_by_name(username)
        if user_id is None:
            return
        friend_ls = []
        sql_query = """
                SELECT *
                FROM relations
                WHERE user_Id = '{user_Id}'
            """
        sql_query = sql_query.format(user_Id=user_id)
        self.execute(sql_query)
        result = self.cur.fetchall()
        for each in result:
            friend_ls.append(self.get_username_by_Id(each[1]))
        return friend_ls

    def get_publickey_by_username(self, username):
        sql_query = """
                SELECT publickey
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        ret = self.cur.fetchone()
        if ret:
            return ret[0]
        else:
            return None

    def send_message(self, sender_name, receiver_name, message):
        sql_query = """
                UPDATE relations
                SET message_sending = '{message}'
                WHERE user_Id = '{user_Id}' AND friend_Id = '{friend_Id}'
            """
        sql_query = sql_query.format(message=message,
                                     user_Id=self.get_userId_by_name(sender_name),
                                     friend_Id=self.get_userId_by_name(receiver_name))
        self.execute(sql_query)

    def receive_message(self, receiver_name, sender_name):
        sql_query = """
                SELECT message_sending
                FROM relations
                WHERE user_Id = '{user_Id}' AND friend_Id = '{friend_Id}'
            """
        sql_query = sql_query.format(message=message,
                                     user_Id=self.get_userId_by_name(receiver_name),
                                     friend_Id=self.get_userId_by_name(sender_name))
        self.execute(sql_query)
