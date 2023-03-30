import random
import uuid
from model.data import my_shop

class Product():
    def __init__(self, name, expiry, category ):         
        self.product_id = str(uuid.uuid4())
        self.serial_nr = random.randint(10000,100000)          #generating a random serial number
        self.name = name 
        self.expiry = expiry
        self.category = category
        self.qty = random.randint(1,50)                        #generating a random quantity to simulate the stock
        self.reason = ""                                       #reason for removal
        self.reorder = False                                   #set the reorder to False by default
        self.itemsSoldInOneWeek = random.randint(1,50)         #generating a random number of items sold in one week to simulate the sales
        self.price= random.randint(1,50)                       #generating a random price to simulate the price of the product
                                                                
    def setQuantity(self, amount):                             #set the quantity of the product
        self.qty += int(amount)                                #add the wanted amount to the total quantity
    def sell(self, amount):
        #self.qty -= int(amount)                       #subtract the amount sold now from the total quantity
        self.itemsSoldInOneWeek += int(amount)        #add the amount sold now to the items sold in one week
        if self.qty == 0:                             #if the quantity is 0, remove the product from the inventory
            my_shop.removeProduct(self)
 
    def removeFromInventory(self, reason):
        self.quantity = "Removed"                     #set the quantity to "Removed" to say that the product is discontinued
        self.reason = reason                          #set the reason for removal
    def setReorder(self):                             
        if self.itemsSoldInOneWeek > self.qty:
            self.reorder = True                       #if the items sold in one week are more than the quantity, set the reorder to True         
            return self                               #and return the product to display it in the API
    def manipulateQty(self, amount):
        self.qty -= int(amount)                       #add the amount to the total quantity
        