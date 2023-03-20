# test_with_pytest.py
from _pytest.fixtures import fixture

from model.Customer import Customer
from model.Shop import Shop


@fixture
def exampleCustomer1():
    c1 = Customer("Markus Muelle", "markus.mueller@email.test", "1101 Vienna", "10.09.2001")
    return c1

def test_customer_add(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    assert exampleCustomer1 in shop.customers
    # try adding again
    shop.addCustomer(exampleCustomer1)
    assert len(shop.customers) == 1 # should be added only once

