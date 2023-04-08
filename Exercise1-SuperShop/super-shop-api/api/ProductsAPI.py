from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Customer import Customer
from model.Product import Product
from model.data import my_shop

ProductAPI = Namespace('product',
                       description='Product Management')

@ProductAPI.route('/')
class AddProductA(Resource):
    @ProductAPI.doc(description="Get a list of all products") 
    def get(self):                        # get a list of all products
        return jsonify(my_shop.products)  # return the list of products
    @ProductAPI.doc(description="Add Product",params={'name': 'Product name',
                            'expiry': 'expiry date',
                            'category': 'product category'})
    def post(self):            # add a new product
        # get the post parameters
        args = request.args    # get the post parameters
        name = args['name']     # store them in the variables
        expiry = args['expiry'] 
        category = args['category']

        new_product = Product(name, expiry, category)   # create a new product
        # add the product
        my_shop.addProduct(new_product)          # add the new product to the shop
        return jsonify(new_product)              # return the added product
    
@ProductAPI.route('/<product_id>')
class SpecificProductOps(Resource):
    @ProductAPI.doc(description="Get data about a particular product")
    def get(self, product_id):                       # get a specific product by id
        search_result = my_shop.getProduct(product_id)      # search for the product
        return jsonify(search_result)                       # return the product
    @ProductAPI.doc(description="Delete an existing product")
    def delete(self, product_id):           # delete a product
        p = my_shop.getProduct(product_id)  # get the product 
        if not p:                          # check if the product exists
            return jsonify("Product ID {product_id} was not found")
        my_shop.removeProduct(p)            # remove the product
        return jsonify("Product with ID {product_id} was removed")
    
    @ProductAPI.doc(description = "Change the stock of existing product",
                    params = {'quantity' : 'quantity'})
    def put(self, product_id):            # change the quantity of a product
        p = my_shop.getProduct(product_id) # get the product
        args = request.args                # get the post parameters
        amount = args['quantity']
        try:                         # check if the quantity is an integer
            int(amount)
        except:
            return jsonify("Quantity must be a integer")    # if not return an error message 
        if not p:            # check if the product exists
            return jsonify(f"Product ID {product_id} was not found")
        p.setQuantity(amount)          # change the quantity of the product
        return jsonify(f"Quantity of a product was changed to {p.qty}")  # return the new quantity
    
@ProductAPI.route('/sell')
class ProductSales(Resource):
    @ProductAPI.doc(description="Sell a product", params={'customer_id': 'Customer ID','product_id': 'Product ID', 'quantity': 'Quantity'})
    def put(self):          # sell a product
        args = request.args # get the post parameters
        quantity = args['quantity']   # store them in the variables
        customer_id = args['customer_id']
        product_id = args['product_id']
        c = my_shop.getCustomer(customer_id)       # get the customer
        p = my_shop.getProduct(product_id)         # get the product
        try:                  # check if the quantity is an integer
            int(quantity)
        except:
            return jsonify("Quantity must be a integer")  # if not return an error message
        if not p:          # check if the product exists
            return jsonify(f"Product ID {product_id} was not found")
        elif not c:        # check if the customer exists
            return jsonify(f"Customer ID {customer_id} was not found")
        elif p.qty < int(quantity):     # check if the product is in stock
            return jsonify(f"Product {p.name} is out of stock")
        p.sell(quantity)                  # sell the product
        c.buyProduct(p.name, quantity)      # add the product to the customer's bought products history
        return jsonify(f"Product {p.name} was sold to {c.name}. Products left: {p.qty},{c.name} bought these products: {c.boughtProducts} so far.") 
    
@ProductAPI.route('/remove')
class RemoveProduct(Resource):
    @ProductAPI.doc(description="Remove a product from inventory", params={'product_id': 'Product ID', 'reason': 'Reason for removal'})
    def delete(self):          # remove a product from inventory
        args = request.args    # get the post parameters
        product_id = args['product_id']     # store them in the variables
        reason = args['reason']
        p = my_shop.getProduct(product_id)       # get the product
        if not p:                                # check if the product exists
            return jsonify(f"Product ID {product_id} was not found")
        p.removeFromInventory(reason)            # remove the product from inventory with a reason
        return jsonify(f"Product {p.name} was removed from inventory. Reason: {p.reason}")
@ProductAPI.route('/reorder')
class ReorderProduct(Resource):
    @ProductAPI.doc(description="Display list of products that need to be reordered")
    def get(self):         # get a list of products that need to be reordered
        reordered_products = []                        #create empty list
        for product in my_shop.products:               #going through products
            if product.setReorder() != None:           #if product needs to be reordered  pozri ci tam nie je None
                reordered_products.append(product.setReorder())        #add product to list
        return jsonify(reordered_products)        #return list of products that need to be reordered