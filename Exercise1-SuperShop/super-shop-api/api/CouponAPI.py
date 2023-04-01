from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Coupon import Coupon
from model.data import my_shop

CouponAPI = Namespace('coupon', description='Coupon Management')

@CouponAPI.route('/')
class GeneralCouponOps(Resource):
    @CouponAPI.doc(description="Add a new coupon",
                   params = {"coupon_number":"Coupon Number 10 digits","category":"Product Category","discount_per":"Discount Percentage","date":"Validity Date"})
    def post(self):
        args = request.args
        coupon_number = args['coupon_number']
        v_date = args['date']
        discount_per = args['discount_per']
        category = args['category']
        try:
            int(coupon_number),int(discount_per)
        except:
            return jsonify("Coupon number and Discount percentage must be a integer")
        if len(coupon_number) != 10:
            return jsonify(f"Coupon number must be 10 integers long")
        else:
            new_coupon = Coupon(coupon_number, v_date, discount_per, category)
            my_shop.addCoupon(new_coupon)
            return jsonify(new_coupon)
    @CouponAPI.doc(description="Get a list of all coupons")
    def get(self):
        return jsonify(my_shop.coupons)
        