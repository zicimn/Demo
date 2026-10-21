def to_index(
    provider
) -> dict:
    return {
        "id":provider.id,
        "name":provider.provider_name,
        "ico":provider.ico
    }

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
