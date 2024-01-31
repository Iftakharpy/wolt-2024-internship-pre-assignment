import pytest
from app.delivery_fee.models import DeliveryFee


edge_cases_for_numeric_fields = [None,
                                 [1, 2, 3], [], {}, {"a": 1, "b": 2}, "invalid"]


# Test __add__
def test_delivery_fee__add__with_valid_data():
    # Try with valid data
    fee = DeliveryFee(delivery_fee=100)
    fee = fee + 100
    assert fee.delivery_fee == 200


@pytest.mark.parametrize("delivery_fee", edge_cases_for_numeric_fields)
def test_delivery_fee__add__with_invalid_data(delivery_fee):
    # Try with invalid data
    with pytest.raises(TypeError):
        DeliveryFee(0) + delivery_fee


# Test __sub__
def test_delivery_fee__sub__with_valid_data():
    # Try with valid data
    fee = DeliveryFee(delivery_fee=100)
    fee = fee - 100
    assert fee == 0


@pytest.mark.parametrize("delivery_fee", edge_cases_for_numeric_fields)
def test_delivery_fee__sub__with_invalid_data(delivery_fee):
    # Try with invalid data
    fee = DeliveryFee(delivery_fee=100)
    with pytest.raises(TypeError):
        fee = delivery_fee - delivery_fee


# Test __mul__
def test_delivery_fee__mul__with_valid_data():
    # Try with valid data
    fee = DeliveryFee(delivery_fee=100)
    fee = fee * 100
    assert fee == 10000


@pytest.mark.parametrize("delivery_fee", edge_cases_for_numeric_fields)
def test_delivery_fee__mul__with_invalid_data(delivery_fee):
    # Try with invalid data
    fee = DeliveryFee(delivery_fee=100)
    with pytest.raises(TypeError):
        fee = fee * delivery_fee


# Test __div__
def test_delivery_fee__div__with_valid_data():
    # Try with valid data
    fee = DeliveryFee(delivery_fee=100)
    fee = fee / 100
    assert fee == 1


@pytest.mark.parametrize("delivery_fee", edge_cases_for_numeric_fields)
def test_delivery_fee__div__with_invalid_data(delivery_fee):
    # Try with invalid data
    fee = DeliveryFee(delivery_fee=100)
    with pytest.raises(TypeError):
        fee = fee / delivery_fee


# Test __gt__
def test_delivery_fee__gt__with_valid_data():
    # Try with valid data
    fee = DeliveryFee(delivery_fee=100)
    assert fee > 50
    assert not (fee > 100)


@pytest.mark.parametrize("delivery_fee", edge_cases_for_numeric_fields)
def test_delivery_fee__gt__with_invalid_data(delivery_fee):
    # Try with invalid data
    fee = DeliveryFee(delivery_fee=100)
    with pytest.raises(TypeError):
        fee > delivery_fee


# Test __ge__
def test_delivery_fee__ge__with_valid_data():
    # Try with valid data
    fee = DeliveryFee(delivery_fee=100)
    assert fee >= 100


@pytest.mark.parametrize("delivery_fee", edge_cases_for_numeric_fields)
def test_delivery_fee__ge__with_invalid_data(delivery_fee):
    # Try with invalid data
    fee = DeliveryFee(delivery_fee=100)
    with pytest.raises(TypeError):
        fee >= delivery_fee


# Test __lt__
def test_delivery_fee__lt__with_valid_data():
    # Try with valid data
    fee = DeliveryFee(delivery_fee=100)
    assert fee < 200
    assert not (fee < 99)


@pytest.mark.parametrize("delivery_fee", edge_cases_for_numeric_fields)
def test_delivery_fee__lt__with_invalid_data(delivery_fee):
    # Try with invalid data
    fee = DeliveryFee(delivery_fee=100)
    with pytest.raises(TypeError):
        fee < delivery_fee


# Test __le__
def test_delivery_fee__le__with_valid_data():
    # Try with valid data
    fee = DeliveryFee(delivery_fee=100)
    assert fee <= 100


@pytest.mark.parametrize("delivery_fee", edge_cases_for_numeric_fields)
def test_delivery_fee__le__with_invalid_data(delivery_fee):
    # Try with invalid data
    fee = DeliveryFee(delivery_fee=100)
    with pytest.raises(TypeError):
        fee <= delivery_fee


# Test __eq__
def test_delivery_fee__eq__with_valid_data():
    # Try with valid data
    fee = DeliveryFee(delivery_fee=100)
    assert fee == 100
    assert not (fee == 101)
    assert not (fee == 99)


@pytest.mark.parametrize("delivery_fee", edge_cases_for_numeric_fields)
def test_delivery_fee__eq__with_invalid_data(delivery_fee):
    # Try with invalid data
    fee = DeliveryFee(delivery_fee=100)
    with pytest.raises(TypeError):
        fee == delivery_fee


# Test __ne__
def test_delivery_fee__ne__with_valid_data():
    # Try with valid data
    fee = DeliveryFee(delivery_fee=100)
    assert fee != 200
    assert not (fee != 100)


@pytest.mark.parametrize("delivery_fee", edge_cases_for_numeric_fields)
def test_delivery_fee__ne__with_invalid_data(delivery_fee):
    # Try with invalid data
    fee = DeliveryFee(delivery_fee=100)
    with pytest.raises(TypeError):
        fee != delivery_fee
