import random
import uuid
from model.data import my_shop

class Product():
    def __init__(self, name, expiry, category ):
        self.product_id = str(uuid.uuid4())
        self.serial_nr = random.randint(10000,100000)
        self.name = name
        self.expiry = expiry
        self.category = category
        self.qty = 0
    def setQuantity(self, amount):
        self.qty += int(amount)
    def sell(self, amount):
        self.qty -= int(amount)
        if self.qty == 0:
            my_shop.removeProduct(self)
