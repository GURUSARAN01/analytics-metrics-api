from app.services import calculate_revenue

def test_calculate_total_revenue():
    result = calculate_revenue()
    assert result["total_revenue"] == 635.74
    assert result["transaction_count"] == 5

def test_calculate_revenue_by_country():
    result = calculate_revenue(country="DE")

    assert result["total_revenue"] == 210.49
    assert result["transaction_count"] == 2

def test_calculate_revenue_with_minimum():
    result = calculate_revenue(min_revenue=100)

    assert result["total_revenue"] == 470.75
    assert result["transaction_count"] == 3

def test_calculate_revenue_by_country_and_minimum():
    result = calculate_revenue(country="DE",min_revenue=100,)

    assert result["total_revenue"] == 120.50
    assert result["transaction_count"] ==  1