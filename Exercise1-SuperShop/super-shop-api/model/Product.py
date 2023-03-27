import random
import uuid

class Product():
    def __init__(self, name, expiry, category, qty ):
        self.product_id = str(uuid.uuid4())
        self.serial_nr = random.randint(10000,100000)
        self.name = name
        self.expiry = expiry
        self.category = category
        self.qty = qty
