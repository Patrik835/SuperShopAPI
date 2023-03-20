# the instance of shop, where all data is stored.
from model.Customer import Customer
from model.Shop import Shop

my_shop = Shop()

# Test data
c1 = Customer("Markus Muelle", "markus.mueller@email.test", "1101 Vienna", "10.09.2001")
my_shop.addCustomer(c1)
