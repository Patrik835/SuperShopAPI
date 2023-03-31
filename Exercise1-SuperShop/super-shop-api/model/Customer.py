import uuid
import random
import ccard
import datetime

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
        self.bonus_points = 0
        self.credit_card_nr = ccard.mastercard()
        self.orders = []
        self.returnable= []

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
        self.boughtProducts[product] = [qty,datetime.date.today()]
    def addToCart(self, product, qty):                #add product to shopping cart
        if product in self.shoppingCart:              #if the product is already in the shopping cart, add just the quantity
            self.shoppingCart[product] += qty
            if self.shoppingCart[product] <= 0:
                self.shoppingCart.pop(product)
        elif qty > 0:
            self.shoppingCart[product] = qty          #else the product is not in the shopping cart, add the product and the quantity
        else:
            pass 
    def verifyCreditCard(self, ccnr):
        if ccnr == self.credit_card_nr and len(str(self.credit_card_nr == 16)):
            return True
        else:
            return False
    def sentOrder(self, product, qty):
        self.shoppingCart[product] -= qty
        self.boughtProducts[product] = [qty,datetime.date.today()]
        
    def updateShoppingCart(self):
        keys_to_remove = []
        for product in self.shoppingCart:
            if self.shoppingCart[product] <= 0:
                keys_to_remove.append(product)
        for key in keys_to_remove:
            self.shoppingCart.pop(key)

    def addBonusPoints(self, points):
        self.bonus_points += int(points)
    def getBonusPoints(self):
        return self.bonus_points
