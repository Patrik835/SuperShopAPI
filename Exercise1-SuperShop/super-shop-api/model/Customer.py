import uuid
import random

class Customer:
    def __init__(self, name, email, address, dob):
        self.customer_id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.email = email
        self.bonus_points = 0
        self.status = "unverified"
        self.verification_token = str(uuid.uuid4())[:5]
        self.dob = dob
        self.temporaryPassword = ""
        self.password = random.randint(10000,100000)
        self.boughtProducts = {}
        self.shoppingCart = {}

    def verify(self, token):
        if self.verification_token == token:
            self.status = "verified"
            self.verification_token = None
        return self.status == "verified"
    def setTemporaryPassword(self,temporaryPassword):
        self.temporaryPassword=temporaryPassword
    def resetPassword(self,new_pw):
        self.password = new_pw
        self.temporaryPassword = ''
    def buyProduct(self,product, qty):
        if product in self.boughtProducts:
            self.boughtProducts[product] += qty
        else:
            self.boughtProducts[product] = qty

