'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''
import base64
import json

from bottle import route, get, post, error, request, static_file, template, response

import model
import ssl
import view

page_view = view.View()


# -----------------------------------------------------------------------------
# Static file paths
# -----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')


# -----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')


# -----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')


# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------

# Redirect to login
@get('/')
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()


# -----------------------------------------------------------------------------
@get('/register')
def get_register_controller():
    '''
        get_login

        Serves the login page
    '''
    return model.register_form()


# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    return model.login_form()


@get('/get-public-key')
def get_public_key():
    # print(model.loadKeys()[1].save_pkcs1('PEM'))
    # # response.content_type = 'text/plain'
    # response.content_type = 'application/json'
    # return model.loadKeys()[1].save_pkcs1('PEM')
    public_key_pem = model.loadKeys()[1]
    print(public_key_pem)
    response.content_type = 'application/json'
    return json.dumps({'publicKey': public_key_pem})


# -----------------------------------------------------------------------------
@post('/register')
def post_register():
    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    public_key = request.forms.get('public_key')

    print(username, password, "\n", public_key)
    # Call the appropriate method
    return model.register(username, password, public_key)


# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')

    # encrypted_password = request.json['encryptedPassword']
    # password=model.decrypt(encrypted_password,model.loadKeys()[0])

    # Call the appropriate method
    return model.login_check(username, password)


# -----------------------------------------------------------------------------
# print friend list
@get('/friendlist')
# @app.route('/friendlist', methods=['GET'])
def get_friendlist(condition, friend_list, header="header", tailer="tailer"):
    username = request.forms.get('username')

    if condition == True:
        body_template = template('friendlist.tpl', name=username, friendlist=friend_list, title='Friends List')
        header_template = page_view.load_template(header)
        tailer_template = page_view.load_template(tailer)

        rendered_template = page_view.render(
            body_template=body_template,
            header_template=header_template,
            tailer_template=tailer_template)

        return rendered_template

        # return model.friends_list(username)


@post('/friendlist')
def post_friendlist():
    '''
        post_login

        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    friendname = request.forms.get('friendname')
    # Handle the form processing
    return model.choose_messagetype(friendname)


# -----------------------------------------------------------------------------

@get('/choosemessagetype')
def get_choosemessagetype(friend, header="header", tailer="tailer"):
    '''
        get_about

        Serves the about page
    '''
    body_template = template('choosemessagetype.tpl', friendname=friend)
    header_template = page_view.load_template(header)
    tailer_template = page_view.load_template(tailer)

    rendered_template = page_view.render(
        body_template=body_template,
        header_template=header_template,
        tailer_template=tailer_template)

    return rendered_template


@get('/send_message')
def send_message():
    # replace this with your code to display a form to send a message to the selected friend
    return model.send_message()
    # return f'Send a message to {friend}'


# -----------------------------------------------------------------------------

@post('/send_message')
def post_sendmessage():
    '''
        post_login

        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    message = request.forms.get('message')
    sender=request.forms.get('sender')
    receiver=request.forms.get('receiver')
    """SQL method here"""

    return model.show_message(message,sender,receiver)


@get('/show_message')
def get_showmessage(message, header="header", tailer="tailer"):
    # replace this with your code to display a form to send a message to the selected friend
    # return f'Send a message to {friend}'

    body_template = template('show_message.tpl', message=message)
    header_template = page_view.load_template(header)
    tailer_template = page_view.load_template(tailer)

    rendered_template = page_view.render(
        body_template=body_template,
        header_template=header_template,
        tailer_template=tailer_template)

    return rendered_template
@get('/receive_form')
def show_receive_form():
    # replace this with your code to display a form to send a message to the selected friend
    return model.receive_form()
@post('/receive_form')
def receive_form():

    receiver_name = request.forms.get('receiver')
    friendname = request.forms.get('sender')
    message = model.get_receivemessage(receiver_name,friendname)
    return get_receivemessage(message)
@get('/receive_message')
def get_receivemessage(message,header="header", tailer="tailer"):
    # replace this with your code to display a form to send a message to the selected friend
    # return f'Send a message to {friend}'
    print(message)
    if message == None:
        message = "No message received"
    body_template = template('receive_message.tpl', message=message)
    header_template = page_view.load_template(header)
    tailer_template = page_view.load_template(tailer)

    rendered_template = page_view.render(
        body_template=body_template,
        header_template=header_template,
        tailer_template=tailer_template)

    return rendered_template


@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()


# -----------------------------------------------------------------------------

# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)


# -----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@error(404)
def error(error):
    return model.handle_errors(error)
