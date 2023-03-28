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
    def get(self):
        return jsonify(my_shop.products)
    @ProductAPI.doc(params={'name': 'Product name',
                            'expiry': 'expiry date',
                            'category': 'product category'})
    def post(self):
        # get the post parameters
        args = request.args
        name = args['name']
        expiry = args['expiry']
        category = args['category']

        new_product = Product(name, expiry, category)
        # add the product
        my_shop.addProduct(new_product)
        return jsonify(new_product)
    
@ProductAPI.route('/<product_id>')
class SpecificProductOps(Resource):
    @ProductAPI.doc(description="Get data about a particular product")
    def get(self, product_id):
        search_result = my_shop.getProduct(product_id)
        return jsonify(search_result)
    @ProductAPI.doc(description="Delete an existing product")
    def delete(self, product_id):
        p = my_shop.getProduct(product_id)
        if not p:
            return jsonify("Product ID {product_id} was not found")
        my_shop.removeProduct(p)
        return jsonify("Product with ID {product_id} was removed")
    
    @ProductAPI.doc(description = "Change the stock of existing product",
                    params = {'quantity' : 'quantity'})
    def put(self, product_id):
        p = my_shop.getProduct(product_id)
        args = request.args
        amount = args['quantity']
        try:
            amount = int(amount)
        except:
            return jsonify("Quantity must be a integer")    
        if not p:
            return jsonify(f"Product ID {product_id} was not found")
        p.setQuantity(amount)
        return jsonify(f"Quantity of a product was changed to {p.qty}")
    
@ProductAPI.route('/sell')
class ProductSales(Resource):
    @ProductAPI.doc(description="Sell a product", params={'customer_id': 'Customer ID','product_id': 'Product ID', 'quantity': 'Quantity'})
    def put(self):
        args = request.args
        quantity = args['quantity']
        customer_id = args['customer_id']
        product_id = args['product_id']
        c = my_shop.getCustomer(customer_id)
        p = my_shop.getProduct(product_id)
        try:
            quantity = int(quantity)
        except:
            return jsonify("Quantity must be a integer") 
        if not p:
            return jsonify(f"Product ID {product_id} was not found")
        elif not c:
            return jsonify(f"Customer ID {customer_id} was not found")
        elif p.qty < int(quantity):
            return jsonify(f"Product {p.name} is out of stock")
        p.sell(quantity)
        c.buyProduct(p.name, quantity)     
        return jsonify(f"Product {p.name} was sold to {c.name}. Products left: {p.qty},{c.name} bought these products: {c.boughtProducts} so far.")
@ProductAPI.route('/remove')
class RemoveProduct(Resource):
    @ProductAPI.doc(description="Remove a product", params={'product_id': 'Product ID'})
    def remove(self):
        args = request.args
        product_id = args['product_id']