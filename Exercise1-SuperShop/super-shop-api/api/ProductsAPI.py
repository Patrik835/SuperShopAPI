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
        c = my_shop.getProduct(product_id)
        if not c:
            return jsonify("Product ID {product_id} was not found")
        my_shop.removeProduct(c)
        return jsonify("Product with ID {product_id} was removed")

