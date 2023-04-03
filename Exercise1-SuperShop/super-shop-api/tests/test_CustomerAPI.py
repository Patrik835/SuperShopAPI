from _pytest.fixtures import fixture
from model.Customer import Customer
from _pytest.fixtures import fixture
from model.Shop import Shop
from model.Customer import Customer
from model.Product import Product
from model.Coupon import Coupon
import datetime

@fixture
def exampleCustomer1():
    c1 = Customer("Markus Muelle", "markus.mueller@email.test", "1101 Vienna", "10.09.2001")
    return c1

@fixture
def product1():
    prod1 = Product("Product 1", "26.06.2023", "bicycle")
    return prod1

@fixture
def coupon1():
    coup1 = Coupon(1111111111, "26.06.2023", 15 , "bicycle")
    return coup1

def test_shop_init():
    shop = Shop()
    assert shop.customers == []
    assert shop.products == []
    assert shop.coupons == []

# testing of customers
def test_customer_add(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    assert exampleCustomer1 in shop.customers
    # try adding again
    shop.addCustomer(exampleCustomer1)
    assert len(shop.customers) == 1 # should be added only once

def test_removeCustomer(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    assert len(shop.customers) == 1
    shop.removeCustomer(exampleCustomer1)
    assert len(shop.customers) == 0

def test_getCustomer(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    assert shop.getCustomer(exampleCustomer1.customer_id) == exampleCustomer1
    assert shop.getCustomer("sdsdsfdfdscsdc") == None
    shop.removeCustomer(exampleCustomer1)
    assert shop.getCustomer(exampleCustomer1.customer_id) == None

def test_getCustomerbyEmail(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    assert shop.getCustomerbyEmail(exampleCustomer1.email) == exampleCustomer1
    assert shop.getCustomerbyEmail("sdsdsfdfdscsdc") == None
    shop.removeCustomer(exampleCustomer1)
    assert shop.getCustomerbyEmail(exampleCustomer1.customer_id) == None

def test_pwreset(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    exampleCustomer1.setTemporaryPassword("test_pw")
    assert exampleCustomer1.temporaryPassword == "test_pw"
    exampleCustomer1.resetPassword("new_test_pw")
    assert exampleCustomer1.password == "new_test_pw"
    assert exampleCustomer1.temporaryPassword == ''
#testing of products
def test_addProduct(product1):
    shop = Shop()
    shop.addProduct(product1)
    assert product1 in shop.products
    # try adding again
    shop.addProduct(product1)
    assert len(shop.products) == 1 # should be added only once

def test_removeProduct(product1):
    shop = Shop()
    shop.addProduct(product1)
    assert len(shop.products) == 1
    shop.removeProduct(product1)
    assert len(shop.products) == 0

def test_getProduct(product1):
    shop = Shop()
    shop.addProduct(product1)
    assert shop.getProduct(product1.product_id) == product1
    assert shop.getProduct("hghgh") == None
    shop.removeProduct(product1)
    assert shop.getProduct(product1.product_id) == None
#test coupons
def test_addCoupon(coupon1):
    shop = Shop()
    shop.addCoupon(coupon1)
    assert coupon1 in shop.coupons
    # try adding again
    shop.addCoupon(coupon1)
    assert len(shop.coupons) == 1 # should be added only once

def test_getCoupon(coupon1):
    shop = Shop()
    shop.addCoupon(coupon1)
    assert shop.getCoupon(coupon1.number) == coupon1
    assert shop.getCoupon("hghgh") == None

#test funcionality
#product methods
def test_setQuantity(product1):
    shop = Shop()
    shop.addProduct(product1)
    assert product1.qty == 0
    product1.setQuantity(10)
    assert product1.qty == 10

def test_sellProduct(product1):
    shop = Shop()
    shop.addProduct(product1)
    product1.setQuantity(10)
    assert product1.itemsSoldInOneWeek == 0
    product1.sell(10)
    assert product1.itemsSoldInOneWeek == 10
    assert product1.qty == 0

def test_removeFromInventory(product1):
    shop = Shop()
    shop.addProduct(product1)
    product1.removeFromInventory("Damaged")
    assert product1.qty == "Removed"
    assert product1.reason == "Damaged"
    
def test_setReorder(product1):
    shop = Shop()
    shop.addProduct(product1)
    product1.setQuantity(15)
    product1.sell(10)
    product1.setReorder()
    assert product1.reorder == True
    product1.setQuantity(20)
    product1.setReorder()
    assert product1.reorder == False
#customer methods
def test_verify(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    exampleCustomer1.verify(exampleCustomer1.verification_token)
    assert exampleCustomer1.status == "verified"
    assert exampleCustomer1.verification_token == None

def test_buyProduct(exampleCustomer1,product1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    shop.addProduct(product1)
    product1.setQuantity(10)
    exampleCustomer1.buyProduct(product1, 5)
    assert exampleCustomer1.boughtProducts[product1] == [5, datetime.date.today()]

def test_shopSimulation(exampleCustomer1,product1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    shop.addProduct(product1)
    product1.setQuantity(20)
    exampleCustomer1.addToCart(product1, 5)
    assert exampleCustomer1.shoppingCart[product1] == 5
    exampleCustomer1.addToCart(product1, 5)
    assert exampleCustomer1.shoppingCart[product1] == 10
    assert exampleCustomer1.verifyCreditCard(4411022) == False
    assert exampleCustomer1.verifyCreditCard(exampleCustomer1.credit_card_nr) == True
    price = exampleCustomer1.shoppingCart[product1] * product1.price
    exampleCustomer1.sentOrder(product1, exampleCustomer1.shoppingCart[product1])
    product1.sell(10)
    assert exampleCustomer1.boughtProducts[product1] == [10, datetime.date.today()]
    exampleCustomer1.updateShoppingCart()
    assert (product1 not in exampleCustomer1.shoppingCart) == True
    assert product1.itemsSoldInOneWeek == 10
    exampleCustomer1.addBonusPoints(price)
    assert exampleCustomer1.getBonusPoints() == price
