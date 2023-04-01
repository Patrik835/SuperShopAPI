from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Customer import Customer
from model.data import my_shop

import random
import datetime
import uuid

CustomerAPI = Namespace('customer',
                        description='Customer Management')


@CustomerAPI.route('/')
class GeneralCustomerOps(Resource):
    @CustomerAPI.doc(description="Get a list of all customers")
    def get(self):
        return jsonify(my_shop.customers)

    @CustomerAPI.doc(
        description="Register a new customer",
        params={'address': 'Customers address',
                'name': 'Customers name',
                'email': 'Customer Email',
                'dob': 'Customer birthday'})
    def post(self):
        # get the post parameters
        args = request.args
        name = args['name']
        email = args['email']
        address = args['address']
        dob = args['dob']
        new_customer = Customer(name, email, address, dob)
        # add the customer
        if my_shop.addCustomer(new_customer):
            return jsonify(new_customer)
        else:
            return jsonify("Customer with the email address already exists")


@CustomerAPI.route('/<customer_id>')
class SpecificCustomerOps(Resource):
    @CustomerAPI.doc(description="Get data about a particular customer")
    def get(self, customer_id):
        search_result = my_shop.getCustomer(customer_id)
        return jsonify(search_result)  # this is automatically jsonified by flask-restx

    @CustomerAPI.doc(description="Delete an existing customer")
    def delete(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")
        my_shop.removeCustomer(c)
        return jsonify("Customer with ID {cust_id} was removed")

    @CustomerAPI.doc(
        description="Update customer data",
        params={'address': 'Customers address',
                'name': 'Customers name',
                'email': 'Customer Email',
                'dob': 'Customer birthday'})
    def put(self, customer_id):                   #update customer method
        c = my_shop.getCustomer(customer_id)     #store customer id in c
        if not c:                                #check if the customer id is in the list         
            return jsonify(f"Customer with ID {customer_id} was not found")  #if not return error message
        else:
            args = request.args            # get the post parameters
            name = args['name']            #store new parameters in variables
            address = args['address']
            dob = args['dob']
            c.name = name                   #update the customer with the new parameters
            c.dob = dob
            c.address = address
            return jsonify(c)               #return the updated customer

        

@CustomerAPI.route('/verify')
class CustomerVerficiation(Resource):
    @CustomerAPI.doc(
        description="Verify customer email address",
        params={'token': 'Verification Token sent by email',
                'email': 'Customer Email'})
    def put(self):
        args = request.args
        token = args['token']
        email = args['email']
        customer = my_shop.getCustomerbyEmail(email)
        if customer is None:
            return jsonify("Customer not found.")
        if customer.verify(token):
            return jsonify("Customer is now verified.")
        else:
            return jsonify("Invalid token.")


@CustomerAPI.route('/<customer_id>/pwreset')
class CustomerPWReset(Resource):
    @CustomerAPI.doc(
        description="Generate a temporary password and send via email.", )
    def post(self, customer_id):
        c=my_shop.getCustomer(customer_id)
        temporaryPassword = random.randint(10000,1000000)
        if not c:
            return jsonify(f"Customer ID {customer_id} was not found")
        else:
            c.setTemporaryPassword(temporaryPassword)
            return jsonify(f"Temp password was send to email:{temporaryPassword}")

    @CustomerAPI.doc(
        description="Allow password reset based on the temporary password",
        params={'temp_pw': 'Password sent by email',
                'new_pw': 'New password'})
    def put(self, customer_id):
        c=my_shop.getCustomer(customer_id)
        args = request.args
        temPassword = args['temp_pw']
        new_pw = args['new_pw']
        if not c:
            return jsonify(f"Customer ID {customer_id} was not found")
        elif temPassword != str(c.temporaryPassword): 
            return jsonify(f"{temPassword} , {c.temporaryPassword} is wrong temporary password")
        else:
            c.resetPassword(new_pw)
            return jsonify(f"New password was changed succesfully. Your new password:{c.password}")
@CustomerAPI.route('/<customer_id>/add2cart')
class CustomerPWReset(Resource):
    @CustomerAPI.doc(
        description="Add products to cart.", params={'product_id': 'Product ID', 'quantity': 'Quantity'})
    def put(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        args = request.args
        product_id = args['product_id']
        quantity = args['quantity']
        p = my_shop.getProduct(product_id)
        try:                                    #check if the quantity is a integer
            int(quantity)
        except:
            return jsonify("Quantity must be a integer")        #if not return error message
        if not c:                                               #check if the customer id is in the list
            return jsonify(f"Customer ID {customer_id} was not found")
        elif not product_id:                                    #check if the product id is in the list
            return jsonify(f"Product ID {product_id} was not found")
        elif p.qty < int(quantity):                                   #check if there is enough quantity of the product in the shop
            return jsonify(f"Product {p.name} is out of stock please add to cart less or equal than {p.qty}") 
        else:
            c.addToCart(product_id,int(quantity))                        #add product to cart
            p.manipulateQty(int(quantity))                                #change the quantity of the product left in the shop
            return jsonify(f"Product with ID {product_id} was added to cart with quantity: {quantity}")
@CustomerAPI.route('/<customer_id>/order')
class CustomerOrder(Resource):
    @CustomerAPI.doc(
        description="Make an order.", params={'shipping_address': 'Shipping Address', 'card_nr': 'Card Number'})
    def post(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        args = request.args
        shipping_address = args['shipping_address']
        card_nr = args['card_nr']
        if not c:                                               #check if the customer id is in the list
            return jsonify(f"Customer ID {customer_id} was not found")
        elif not c.verifyCreditCard(int(card_nr)):
            return jsonify(f"Card number is not valid {c.credit_card_nr}")
        elif not c.shoppingCart:
            return jsonify(f"Shopping cart is empty")
        else:
            total_price = 0                                 #var to calculate the total price of the order
            for prod in c.shoppingCart:                    #loop through the shopping cart
                qty = c.shoppingCart[prod]                 #store the quantity of the product in the cart              
                total_price +=  qty * my_shop.getProduct(prod).price     #calculate the total price
                c.sentOrder(prod, c.shoppingCart[prod])                                #send the order to the shop
                p = my_shop.getProduct(prod)
                p.sell(qty)                            #sell the product
            c.updateShoppingCart()                                     #update the shopping cart
            
            if total_price > int(c.bonus_points*0.1):                  #check if the total price is bigger than value of bonus points
                end_price = total_price - int(c.bonus_points*0.1)      #if yes calculate the end price by subtracting the value of bonus points
            else:                                                #if the price is smaller than the value of bonus points
                c.bonus_points -= total_price*10                  #subtract used bonus points to pay for the order
                end_price = 0                                   #end price is 0            
            c.addBonusPoints(int(end_price))                    #add bonus points to the customer
            send = datetime.date.today()
            dellivery = send + datetime.timedelta(days=3)
            c.orders = [send, dellivery]
            return jsonify(f"Order was sent succesfully to {shipping_address}. You have now: {c.bonus_points} bonsu points") 
@CustomerAPI.route('/<customer_id>/orders')
class CustomerOrders(Resource):
    @CustomerAPI.doc(description="Get data about orders.")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:                                               #check if the customer id is in the list
            return jsonify(f"Customer ID {customer_id} was not found")
        else:
            return jsonify(c.orders)
@CustomerAPI.route('/<customer_id>/returnable')
class Returnable(Resource):
    @CustomerAPI.doc(description="Get products that are still returnable.")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        
        if not c:                                               #check if the customer id is in the list
            return jsonify(f"Customer ID {customer_id} was not found")
        for product in c.boughtProducts:
            lis = c.boughtProducts[product]
            if lis[1] + datetime.timedelta(days=14) > datetime.date.today():
                c.returnable.append(product)
        return jsonify(c.returnable)
@CustomerAPI.route('/<customer_id>/recommendations')
class Reccommendations(Resource):
    @CustomerAPI.doc(description="Get recommendations to customer.")
    def get(self, customer_id):
        top_list = []
        c = my_shop.getCustomer(customer_id)
        if not c:                                               #check if the customer id is in the list
            return jsonify(f"Customer ID {customer_id} was not found")
        sorted_products_by_qty = sorted(c.boughtProducts.items(), key = lambda x:x[1], reverse = True)  #sorting the history dict from biggest to lowest
        sorted_products_by_qty_dict = dict(sorted_products_by_qty)         #converting it back to dictionary
        for product in sorted_products_by_qty_dict:                    #taking first 10 id and appending them to final list
            if len(top_list) <= 10:
                top_list.append(product)
        return jsonify(top_list)

@CustomerAPI.route('/<customer_id>/points')
class Points(Resource):
    @CustomerAPI.doc(description="Get customers bonus points.")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify(f"Customer with id {customer_id} was not found")
        points = c.getBonusPoints()
        return jsonify(f"You have now {points} points.")
    @CustomerAPI.doc(description="Add customers bonus points.", params = {"number_of_pts":"Number of Points"})
    def put(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        args = request.args
        nr_points = args["number_of_pts"]
        if not c:
            return jsonify(f"Customer with id {customer_id} was not found")
        try:                                    #check if the quantity is a integer
            int(nr_points)
        except:
            return jsonify("Quantity must be a integer")        #if not return error message
        c.addBonusPoints(nr_points)
        return jsonify(f"You have succesfully added {nr_points} points.")