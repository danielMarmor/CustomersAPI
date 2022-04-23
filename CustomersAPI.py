from flask import Flask, request, render_template, jsonify, make_response
from Customer import Customer
from CustomersService import CustomerService
from CustomersRepository import CustomersRepository
from db_config import local_session, create_all_entities
from NotFoundException import NotFoundException
from configparser import ConfigParser
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import uuid
import jwt
import os

import json

template_dir = os.path.abspath('Login/templates')
app = Flask(__name__, template_folder=template_dir)
app = Flask(__name__)
app.static_folder = os.path.abspath('Login/static')

# customers = [
#     Customer(id=1, name='danny', address='tel-aviv'),
#     Customer(id=2, name='marina', address='beer sheav'),
#     Customer(id=3, name='david', address='herzeliya')
# ]

# customers = [
#     Customer(1, 'danny', 'tel-aviv'),
#     Customer(2, 'marina', 'beer sheav'),
#     Customer(3, 'david', 'herzeliya')
# ]

# INIT CUSTOMERS_API
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

create_all_entities()
repository = CustomersRepository(local_session)
customer_service = CustomerService(repository)
config_file_name = 'config.conf'
config_file_location = os.path.join(ROOT_DIR, config_file_name)
config = ConfigParser()
config.read(config_file_location)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        is_auth = 'Authorization' in request.headers
        if not is_auth:
            token_missing_res = make_response('Token is missing!', 401)
            return token_missing_res
        # AUTHORIZATION
        token = request.headers['Authorization']
        token = token.removeprefix('Bearer ')
        secret_key = config['security']['secret_key']
        try:
            auth_data = jwt.decode(token, secret_key)
        except:
            invalid_token_res = make_response('Token is Invalid!', 401)
            return invalid_token_res
        is_public_id = 'public_id' in auth_data.keys()
        if not is_public_id:
            invalid_token_res = make_response('Token is Invalid!', 401)
            return invalid_token_res
        # PUBLIC ID
        user_public_id = auth_data['public_id']
        current_user = customer_service.get_user_by_public_id(user_public_id)
        if current_user is None:
            invalid_token_res = make_response('Token is Invalid!', 401)
            return invalid_token_res
        # RETURN
        target = f(current_user, *args, **kwargs)
        return target
    return decorated


@app.route('/signup', methods=['POST'])
def signup():
    form_data = request.form
    if form_data is None:
        # 401
        no_form_res = make_response('Could not Verifiy', 401)
        return no_form_res
    # FORM
    is_form = 'username' in form_data.keys() and 'email' in form_data.keys() and 'password' in form_data.keys()
    if not is_form:
        # 401
        no_valid_form_res = make_response('Could not Verifiy', 401)
        return no_valid_form_res
    email = form_data['email']
    username = form_data['username']
    password = form_data['password']
    # USER
    user = customer_service.get_user_by_user_name(username)
    if user is not None:
        # 201
        user_exists_res = make_response('User Already Exists. Please Log in', 202)
        return user_exists_res
    # NEW USER
    customer_service.create_new_user(username, email, password)
    user_created_res = make_response('Succesfuly registered!', 201)
    return user_created_res


@app.route('/login', methods=['POST'])
def login():
    form_data = request.form
    if form_data is None:
        # 401
        no_form_res = make_response('Could not Verifiy', 401,  {'WWW-Authenticate': 'Basic realm="Login Required!"'})
        return no_form_res
    # FORM
    is_form = 'username' in form_data.keys() and 'password' in form_data.keys()
    if not is_form:
        # 401
        no_valid_form_res = make_response('Could not Verifiy', 401,
                                          {'WWW-Authenticate': 'Basic realm="Login Required!"'})
        return no_valid_form_res

    username = form_data['username']
    password = form_data['password']

    # USER
    user = customer_service.get_user_by_user_name(username)
    if user is None:
        # 401
        not_exists_user_res = make_response('Could not Verifiy', 401,
                                            {'WWW-Authenticate': 'Basic realm="User Does Not EXists!"'})
        return not_exists_user_res
    # PASWORD
    is_password = check_password_hash(user.password, password)
    if not is_password:
        not_password_res = make_response('Could not Verifiy', 403,
                                    {'WWW-Authenticate': 'Basic realm="Wrong Password!"'})
        return not_password_res
    # TOKEN
    secret_key = config['security']['secret_key']
    token = jwt.encode({
        'public_id': user.public_id,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, secret_key)
    auth_res = make_response(jsonify({'token': token.decode('utf-8')}), 201)
    return auth_res


@app.route('/users', methods=['GET'])
@token_required
def get_users(current_user, *args, **kwargs):
    if request.method == 'GET':
        try:
            users = customer_service.get_users()
            users_data = json.dumps([usr.serialize for usr in users])
            return users_data
        except Exception as exc:
            return {'status': f'faild, {exc}'}


@app.route('/customers', methods=['GET', 'POST'])
def get_or_post_customers(current_user, *args, **kwargs):
    if request.method == 'GET':
        try:
            customers = customer_service.get_customers()
            customers_data = json.dumps([cust.serialize for cust in customers])
            return customers_data
        except Exception as exc:
            return {'status': f'faild, {exc}'}

    if request.method == 'POST':
        try:
            new_data = request.get_json()
            new_customer = Customer(cust_id=None, name=new_data['name'], address=new_data['address'])
            customer_service.add_customer(new_customer)
            return {'status': 'success'}
        except Exception as exc:
            return {'status': f'faild, {exc}'}


@app.route('/search', methods=['GET'])
@token_required
def get_customers_search(current_user, *args, **kwargs):
    if request.method == 'GET':
        try:
            params = request.args.to_dict()
            customers = customer_service.get_customers_search(**params)
            customers_data = json.dumps([cust.serialize for cust in customers])
            return customers_data
        except Exception as exc:
            return {'status': f'faild, {exc}'}


@app.route('/customers/<int:customer_id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
@token_required
def get_customer_by_id(current_user, *args, **kwargs):
    if request.method == 'GET':
        try:
            customer_id = kwargs['customer_id']
            customer = customer_service.get_customer_by_id(customer_id)
            if customer is None:
                raise NotFoundException('Customer Not Found', Customer, customer_id)
            data = json.dumps(customer.serialize)
            return data
        except NotFoundException as exc:
            return {'status': 'Not Found'}
        except Exception as exc:
            return {'status': f'faild, {exc}'}

    if request.method == 'PUT':
        try:
            customer_id = kwargs['customer_id']
            customer_data = request.get_json()
            customer_service.put_customer(customer_id, customer_data)
            return {'status': 'success'}
        except Exception as exc:
            return {'status': f'faild, {exc}'}

    if request.method == 'PATCH':
        try:
            customer_id = kwargs['customer_id']
            customer_data = request.get_json()
            customer_service.patch_customer(customer_id, customer_data)
            return {'status': 'success'}
        except Exception as exc:
            return {'status': f'faild, {exc}'}

    if request.method == 'DELETE':
        try:
            customer_id = kwargs['customer_id']
            customer_service.remove_customer(customer_id)
            return {'status': 'success'}
        except NotFoundException as exc:
            return {'status': 'Not Found'}
        except Exception as exc:
            return {'status': 'Failed'}


app.run()

