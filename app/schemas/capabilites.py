def to_model_capabilites(capabilites) ->dict:
    return {
        "id":capabilites.id,
        "cap_name":capabilites.cap_name,
        "support_status":capabilites.support_status,
        "is_beta":capabilites.is_beta,
        "note":capabilites.note or None 
    }