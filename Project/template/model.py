'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import os

import sql
import view
import random

import controller

import rsa

privateKeyPath = 'keys/privateKey.pem'
publicKeyPath = 'keys/publicKey.pem'
# Initialise our views, all arguments are defaults for the template
page_view = view.View()

# # Get the app instance
# app = default_app()
#
# # Get the database instance from the app config
# sql_db = app.config['db']
database_args = os.getcwd() + "/database/system.db"
sql_db = sql.SQLDatabase(database_args=database_args)
print(sql_db)


def setup():
    print(333)
    sql_db.database_setup("password")
    # sql_db.add_user("Derrick", "123456", 0)
    # sql_db.add_user("Emily", "123456", 0)
    # sql_db.add_relations("Derrick", "Emily")
    # print(sql_db.get_friend_list("Derrick"))
    # print(sql_db.get_friend_list("Emily"))


def generateKeys():
    # Generate the key pair
    public_key, private_key = rsa.newkeys(2048)
    # Save the private key to a file
    with open(privateKeyPath, 'wb') as private_key_file:
        private_key_pem = private_key.save_pkcs1()
        private_key_file.write(private_key_pem)

    # Save the public key to a file
    with open(publicKeyPath, 'wb') as public_key_file:
        public_key_pem = public_key.save_pkcs1()
        public_key_file.write(public_key_pem)


def loadKeys():
    with open(publicKeyPath, 'rb') as public_key_file:
        public_key_pem = public_key_file.read().decode()
    with open(privateKeyPath, 'rb') as private_key_file:
        private_key_pem = private_key_file.read().decode()
    return private_key_pem, public_key_pem


def encrypt(message, key):
    return rsa.encrypt(message.encode('ascii'), key)


def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except:
        return False


# def sign(message, key):
#     return rsa.sign(message.encode('ascii'), key, 'SHA-1')
#
# def verify(message, signature, key):
#     try:
#         return rsa.verify(message.encode('ascii'), signature, key,) == 'SHA-1'
#     except:
#         return False

# -----------------------------------------------------------------------------
# Index
# -----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")


# -----------------------------------------------------------------------------
# Login
# -----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")


# -----------------------------------------------------------------------------
def register_form():
    return page_view("register")


def register(username, password, publickey):
    sql_db.add_user(username, password, publickey, 0)
    # return page_view("login")
    return page_view("keyGen")


# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default, assume good creds
    login = True

    # Perform login logic here
    if sql_db.check_credentials(username, password):
        friend_list = sql_db.get_friend_list(username)
        return controller.get_friendlist(True, friend_list)
        # return page_view("valid", name=username)
    else:
        return page_view("invalid", reason="Incorrect Account Info!")


def send_message(friend_name):
    return page_view("send_message")

def choose_messagetype(friend):
    '''
        index
        Returns the view for the index
    '''
    return controller.get_choosemessagetype(friend)

def get_receivemessage(receiver_name,chosen_friend):
    message = sql_db.receive_message( receiver_name,chosen_friend)
    print(message)
    return message


def send_message():
    return page_view("send_message")

def receive_form():
    return page_view("receive_form")
# def store_message(message,sender,receiver):
#     sql_db.send_message(message,sender,receiver)
def show_message(message,sender,receiver):
    sql_db.send_message( sender, receiver,message)
    return controller.get_showmessage(message)
# -----------------------------------------------------------------------------
# About
# -----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())


# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.",
              "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
              "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
              "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
              "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
              "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


# -----------------------------------------------------------------------------
# Debug
# -----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


# -----------------------------------------------------------------------------
# 404
# Custom 404 error page
# -----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)
