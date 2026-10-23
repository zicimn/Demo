def to_provider(provider)->dict:
    return {
        "id":provider.id,
        "provider_code":provider.provider_code,
        "provider_name": provider.provider_name,
        "website_url": provider.website_url or None,
    }

    
def to_pdetail(provider)->dict:
    return {
        "id":provider.id,
        "provider_code":provider.provider_code,
        "provider_name": provider.provider_name,
        "website_url": provider.website_url or None,
        "description": provider.description or None,
    }