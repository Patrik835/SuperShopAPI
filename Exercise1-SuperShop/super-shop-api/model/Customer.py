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
        self.boughtProducts = {}                     #dictionary to store the history of bought products
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
    def setTemporaryPassword(self,temporaryPassword):         #set a temporary password
        self.temporaryPassword=temporaryPassword              #set the temporary password to the one given
    def resetPassword(self,new_pw):              #reset the password
        self.password = new_pw                   #set the password to the new password
        self.temporaryPassword = ''              #set the temporary password to empty
    def buyProduct(self,product, qty):           #buy a product
        self.boughtProducts[product] = [qty,datetime.date.today()]       #add the product to the bought products dictionary
    def addToCart(self, product, qty):                #add product to shopping cart
        if product in self.shoppingCart:              #if the product is already in the shopping cart, add just the quantity
            self.shoppingCart[product] += qty         
            if self.shoppingCart[product] <= 0:       #if the quantity is less than or equal to 0, remove the product from the shopping cart
                self.shoppingCart.pop(product)         
        elif qty > 0:                                 
            self.shoppingCart[product] = qty          #else the product is not in the shopping cart, add the product and the quantity
    def verifyCreditCard(self, ccnr):                 #verify the credit card number
        if ccnr == self.credit_card_nr and len(str(self.credit_card_nr == 16)):    #if the credit card number is the same and the lenof the cc number is 16
            return True                               
        else:                                        
            return False
    def sentOrder(self, product, qty):         #send the order
        self.shoppingCart[product] -= qty      #subtract the quantity from the shopping cart
        self.boughtProducts[product] = [qty,datetime.date.today()]    #add the product to the bought products dictionary
        
    def updateShoppingCart(self):          #update the shopping cart
        keys_to_remove = []                #create a list to store the keys to remove
        for product in self.shoppingCart:        #for each product in the shopping cart
            if self.shoppingCart[product] <= 0:  #if the quantity is less than or equal to 0
                keys_to_remove.append(product)   #add the product to the list of keys to remove
        for key in keys_to_remove:               #for each key in the list of keys to remove
            self.shoppingCart.pop(key)           #remove the key from the shopping cart

    def addBonusPoints(self, points):           #add bonus points
        self.bonus_points += int(points)        #add the points to the bonus points 
    def getBonusPoints(self):            #get the bonus points
        return self.bonus_points         #return the bonus points