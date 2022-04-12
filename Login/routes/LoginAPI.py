from flask import Flask, request, render_template, redirect, session
from flask_session import Session
from CustomersService import CustomerService
from CustomersRepository import CustomersRepository
from db_config import local_session, create_all_entities
from configparser import ConfigParser
from werkzeug.security import generate_password_hash, check_password_hash
import os

# INIT CUSTOMERS_API
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

create_all_entities()
repository = CustomersRepository(local_session)
customer_service = CustomerService(repository)
config_file_name = 'config.conf'
config_file_location = os.path.join(ROOT_DIR, config_file_name)
config = ConfigParser()
config.read(config_file_location)

template_dir = os.path.abspath('../templates')
app = Flask(__name__, template_folder=template_dir)
app.static_folder = os.path.abspath('../static')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.route('/', methods=['GET'])
def home():
    return redirect('/signup')


@app.route('/signup', methods=['GET'])
def signup():
    signup_template = render_template('signup.html')
    return signup_template


@app.route('/signup_process', methods=['POST'])
def signup_process():
    form_data = request.form
    if form_data is None:
        signup_response = signup()
        return signup_response

    is_form_valid = 'uname' in form_data.keys() and\
                    'email' in form_data.keys() and\
                    'psw' in form_data.keys() and\
                    'psw-repeat' in form_data.keys()
    if not is_form_valid:
        signup_response = signup()
        return signup_response
    # VALID FORM
    username = form_data['uname']
    email = form_data['email']
    psw = form_data['psw']
    psw_repeat = form_data['psw-repeat']
    # PASSWORD NOT MATCH
    if psw != psw_repeat:
        signup_response = signup()
        return signup_response
    # CREATE USER
    user = customer_service.get_user_by_user_name(username)
    if user is not None:
        # 201
        signup_response = signup()
        return signup_response
    # NEW USER
    try:
        customer_service.create_new_user(username, email, psw)
    except Exception as exc:
        return redirect('/login_err')
    user = customer_service.get_user_by_user_name(username)
    # SAVE IN SESSION
    session['user'] = user
    if 'remember' in form_data.keys():
        session['remember'] = 1
    else:
        session['remember'] = 0
    return redirect('/my_app')


@app.route('/process_form', methods=['POST'])
def process_form():
    form_data = request.form
    if form_data is None:
        # - NO FORM 401
        return redirect('/login_err')

    is_form = 'uname' in form_data.keys() and 'psw' in form_data.keys()
    if not is_form:
        # 401 - NO FORM PARAMS 401
        return redirect('/login_err')
    # VALID FROM
    username = form_data['uname']
    password = form_data['psw']

    user = customer_service.get_user_by_user_name(username)
    if user is None:
        # 403
        return redirect('/login_err')
    # PASWORD
    is_password = check_password_hash(user.password, password)
    if not is_password:
        return redirect('/login_err')
    # SAVE IN SESSION
    session['user'] = user
    if 'remember' in form_data.keys():
        session['remember'] = 1
    else:
        session['remember'] = 0
    return redirect('/my_app')


@app.route('/login', methods=['GET'])
def login():
    # IS LOGGED IN
    is_remember = session and session['user'] and session['remember'] == 1
    if is_remember:
        return redirect('/my_app')
    login_response = render_template('loginForm.html')
    return login_response


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/login')


@app.route('/login_err', methods=['GET'])
def login_err():
    error_response = render_template('login_error.html')
    return error_response


@app.route('/my_app', methods=['GET'])
def my_app():
    user = session.get('user')
    user_name = user.username
    my_app_response = render_template('myApp.html', username=user_name)
    return my_app_response


app.run()

