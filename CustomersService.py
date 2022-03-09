from CustomersRepository import CustomersRepository
from Customer import Customer
from User import User
from NotFoundException import NotFoundException
from operator import attrgetter
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class CustomerService:
    def __init__(self, customers_repository: CustomersRepository):
        self.customers_repository = customers_repository

    # get_users
    def get_users(self):
        users = self.customers_repository.get_all(User)
        return users

    # get_customers
    def get_customers(self):
        customers = self.customers_repository.get_all(Customer)
        return customers

    # get_customers_search
    # search method = acumulative search (AND)
    def get_customers_search(self, **search_params):
        empty = []
        cust_res = []
        customers = self.customers_repository.get_all(Customer)
        search_items = search_params.items()
        for cust in customers:
            is_selected = True
            for search_name, search_value in search_items:
                is_prop = hasattr(cust, search_name)
                if not is_prop:
                    is_selected = False
                    break
                cust_prop = getattr(cust, search_name)
                cust_prop_str = str(cust_prop)
                is_cust = cust_prop_str.upper().find(search_value.upper()) != -1
                if not is_cust:
                    is_selected = False
                    break
            if is_selected:
                cust_res.append(cust)
        return cust_res

    # get_customer_by_id
    def get_customer_by_id(self, customer_id):
        customer = self.customers_repository.get_by_id(Customer, customer_id)
        return customer

    # add_customer
    def add_customer(self, customer):
        customers = self.customers_repository.get_all(Customer)
        new_customer_id = (max(customers, key=attrgetter('cust_id')).cust_id + 1) if len(customers) > 0 else 1
        customer.cust_id = new_customer_id
        self.customers_repository.add(customer)

    # put_customer
    def put_customer(self, customer_id, customer_data):
        customer = self.get_customer_by_id(customer_id)
        # add
        if customer is None:
            new_customer = Customer(cust_id=None, name=customer_data["name"], address=customer_data["address"])
            self.add_customer(new_customer)
            return
        # update
        updated_data = {}
        if 'name' in customer_data.keys():
            updated_data['name'] = customer_data['name']
        else:
            updated_data['name'] = ''
        # address
        if 'address' in customer_data.keys():
            updated_data['address'] = customer_data['address']
        else:
            updated_data['address'] = ''
        self.customers_repository.update(Customer, 'cust_id', customer_id, updated_data)

    # patch_customer
    def patch_customer(self, customer_id, customer_data):
        customer = self.get_customer_by_id(customer_id)
        # add
        if customer is None:
            return
        # update
        del customer_data['cust_id']
        self.customers_repository.update(Customer, 'cust_id', customer_id, customer_data)

    # remove_customer
    def remove_customer(self, customer_id):
        customer = self.get_customer_by_id(customer_id)
        # add
        if customer is None:
            raise NotFoundException('Customer Not Found!', Customer, customer_id)
        self.customers_repository.remove(Customer, 'cust_id', customer_id)

    # get_user_by_user_name
    def get_user_by_user_name(self, username):
        user_cond = (lambda query: query.filter(User.username == username))
        users = self.customers_repository.get_all_by_condition(User, user_cond)
        if len(users) == 0:
            return None
        user = users[0]
        return user

    # get_user_by_public_id
    def get_user_by_public_id(self, public_id):
        user_cond = (lambda query: query.filter(User.public_id == public_id))
        users = self.customers_repository.get_all_by_condition(User, user_cond)
        if len(users) == 0:
            return None
        user = users[0]
        return user

    # create_new_user
    def create_new_user(self, username, email, password):
        new_user = User(public_id=uuid.uuid4(),
                        username=username,
                        email=email,
                        password=generate_password_hash(password))
        self.customers_repository.add(new_user)

