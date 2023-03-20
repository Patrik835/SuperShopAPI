from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Customer import Customer
from model.Product import Product
from model.data import my_shop

ProductAPI = Namespace('product',
                       description='Product Management')


@ProductAPI.route('/')
class AddProductA(Resource):
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
