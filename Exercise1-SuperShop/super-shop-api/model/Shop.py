class Shop:
    def __init__(self):
        self.customers = []
        self.products = []
        self.coupons = []

    def addProduct(self, p):
        self.products.append(p)

    def addCustomer(self, c):
        c1 = self.getCustomerbyEmail(c.email)
        if c1 == None:  # customer does not exist with the given email address
            self.customers.append(c)
            return True
        else:
            return False

    def removeCustomer(self, c): 
        self.customers.remove(c)                 #remove customer from list

    def getCustomer(self, cust_id):
        for c in self.customers:                 #search for customer by id
            if c.customer_id == cust_id:         #if id is found
                return c                         #return customer
    def getCustomerbyEmail(self, email):                      
        for c in self.customers:                  #search for customer by email          
            if c.email == email:                  #if email is found            
                return c                          #return customer                        
    def getProduct(self, product_id):
        for p in self.products:                   #search for product by id
            if p.product_id == product_id:        #if id is found
                return p                          #return product  
    def removeProduct(self, p):                  
        self.products.remove(p)                   #remove product from list
    def addCoupon(self, c):                     #adding coupons
        self.coupons.append(c)
    