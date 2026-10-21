def to_model(model) ->dict:
    return {
        "id" : model.id,
        "model_slug": model.model_slug,
        "display_name": model.display_name,
        "model_version": model.model_version or None,
        "model_family": model.model_family or None,
        "context_length_raw": model.context_length_raw or None,
        "max_output_raw": model.max_output_raw or None,
        "thinking_support": model.thinking_support,
        "default_thinking_mode": model.default_thinking_mode or None,
        "thinking_note": model.thinking_note or None,
        "concurrency_limit":model.concurrency_limit or None,
        "doc_url": model.doc_url or None,
        "description": model.description,
        "provider_id":model.provider_id
    }




