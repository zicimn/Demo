# 供应商输出统一成一份：列表、详情、模型详情里内嵌的 provider 都走这里
def to_provider(provider)->dict:
    return {
        "id":provider.id,
        "provider_code":provider.provider_code,
        "provider_name": provider.provider_name,
        "website_url": provider.website_url or None,
        "description": provider.description or None,
        "ico": provider.ico or None,
    }