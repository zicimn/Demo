def to_model_prices(prices) -> dict:
    return {
        "id" : prices.id,
        "price_type": prices.price_type,
        "time_period": prices.time_period,
        "price": prices.price
    }