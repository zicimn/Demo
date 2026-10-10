# 路由文档

> 基于代码实际定义，截至 2026-10-10

## 路由总览

| 方法 | 路径 | 说明 | 标签 |
|------|------|------|------|
| GET | `/service/display/models/{id}` | 获取模型详情（含供应商、能力、定价） | Display |

> 路由前缀：`/service/display`，定义于 `app/api/service/display.py`

---

## GET `/service/display/models/{id}`

获取单个 AI 模型的完整信息，包括所属供应商、能力列表和定价列表。

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 模型 ID |

### 请求体

无

### 响应

**成功 (200)** — 返回 `Detail` 对象：

```json
{
  "provider": {
    "id": 1,
    "provider_code": "deepseek",
    "provider_name": "DeepSeek",
    "website_url": "https://deepseek.com",
    "status": true,
    "created_at": "2026-01-01T00:00:00",
    "updated_at": "2026-01-01T00:00:00"
  },
  "model": {
    "id": 1,
    "model_slug": "deepseek-chat",
    "display_name": "DeepSeek Chat",
    "model_version": "V3",
    "model_family": "DeepSeek",
    "context_length_raw": "64K",
    "context_length_tokens": null,
    "max_output_raw": "8K",
    "max_output_tokens": null,
    "thinking_support": "both",
    "default_thinking_mode": "thinking",
    "thinking_note": null,
    "concurrency_limit": 10,
    "status": "active",
    "doc_url": "https://api-docs.deepseek.com",
    "description": "DeepSeek 通用对话模型",
    "provider_id": 1,
    "created_at": "2026-01-01T00:00:00",
    "updated_at": "2026-01-01T00:00:00"
  },
  "capabilities": [
    {
      "id": 1,
      "cap_code": "json_output",
      "cap_name": "JSON 输出",
      "support_status": "supported",
      "is_beta": false,
      "note": null,
      "is_active": true,
      "created_at": "2026-01-01T00:00:00",
      "updated_at": "2026-01-01T00:00:00"
    }
  ],
  "prices": [
    {
      "id": 1,
      "price_type": "input",
      "time_period": "peak",
      "price": 2.0,
      "created_at": "2026-01-01T00:00:00",
      "updated_at": "2026-01-01T00:00:00"
    }
  ]
}
```

**未找到 (404)**：

```json
{
  "detail": "模型不存在"
}
```

### 业务逻辑

1. 通过 `selectinload` 预加载供应商、能力、定价关联数据
2. 能力列表仅返回 `is_active = true` 的记录
3. 定价列表返回全部记录（未做时间过滤）

---

## 已定义 Schema（未绑定路由）

以下 Schema 已在 `app/schema/detail.py` 中定义，但尚未被任何路由使用：

| Schema | 说明 |
|--------|------|
| `ModelListResponse` | 模型分页列表（items + total + page + page_size） |
| `ProviderListResponse` | 供应商分页列表（items + total + page + page_size） |
| `ProviderDetailResponse` | 供应商详情（provider + models 列表） |

这些 Schema 预留给后续的列表/详情接口使用。
