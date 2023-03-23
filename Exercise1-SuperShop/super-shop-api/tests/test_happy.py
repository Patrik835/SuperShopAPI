import pytest
def add(x,y):
    return x + y
def test_addfunction():
    assert (add(4,3) == 7)

def capital_case(x):
    return x.upper()
def test_capital_case():
    assert (capital_case('s') == 'S')

@pytest.mark.parametrize('inp, outp',[("3+5", 8), ("2+4", 6), ("6*7", 42)])
def test_eval(inp, outp):
    assert (eval(inp) == outp)