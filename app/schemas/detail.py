def to_detail(
    proivder,
    model,
    capabilities,
    prices
) ->dict:
    return {
        "provider":proivder,
        "model":model,
        "capabilities":capabilities,
        "prices":prices
    }