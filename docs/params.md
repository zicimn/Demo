# 参数文档

> 基于代码实际定义，截至 2026-10-10

---

## 通用说明

- 时间字段统一为 ISO 8601 格式：`YYYY-MM-DDTHH:mm:ss`
- 响应不含统一包装结构（直接返回业务数据）

---

## GET `/service/display/models/{id}`

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 模型 ID（对应 `ai_model.id`） |

### 查询参数

无

### 请求体

无

### 响应体 — `Detail`

| 字段 | 类型 | 说明 |
|------|------|------|
| provider | AiProvider | 所属供应商信息 |
| model | AiModelBase | 模型基本信息 |
| capabilities | AiModelCap[] | 模型能力列表（仅活跃记录） |
| prices | AiModelPrice[] | 模型定价列表 |

---

### AiProvider

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 供应商 ID |
| provider_code | string | 是 | 供应商标识，如 `deepseek` |
| provider_name | string | 是 | 供应商名称，如 `DeepSeek` |
| website_url | string \| null | 否 | 官网/文档地址 |
| status | bool | 是 | 是否启用 |
| created_at | datetime | 是 | 创建时间 |
| updated_at | datetime | 是 | 更新时间 |

---

### AiModelBase

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 模型 ID |
| model_slug | string | 是 | 模型标识，如 `deepseek-chat` |
| display_name | string | 是 | 展示名 |
| model_version | string \| null | 否 | 模型版本 |
| model_family | string \| null | 否 | 模型系列 |
| context_length_raw | string \| null | 否 | 上下文长度原文，如 `64K`、`1M` |
| context_length_tokens | int \| null | 否 | 上下文长度数值（Schema 中保留，ORM 已移除，始终为 null） |
| max_output_raw | string \| null | 否 | 最大输出原文，如 `8K` |
| max_output_tokens | int \| null | 否 | 最大输出数值（Schema 中保留，ORM 已移除，始终为 null） |
| thinking_support | string | 是 | 思考模式：`none` / `non_thinking_only` / `thinking_only` / `both` / `unknown` |
| default_thinking_mode | string \| null | 否 | 默认模式：`non_thinking` / `thinking` / `unknown` |
| thinking_note | string \| null | 否 | 思考模式切换说明 |
| concurrency_limit | int \| null | 否 | 并发限制 |
| status | string | 是 | 状态：`active` / `inactive` / `deprecated` |
| doc_url | string \| null | 否 | 模型文档地址 |
| description | string \| null | 否 | 模型描述 |
| provider_id | int | 是 | 所属供应商 ID |
| created_at | datetime | 是 | 创建时间 |
| updated_at | datetime | 是 | 更新时间 |

> ⚠️ `context_length_tokens` 和 `max_output_tokens` 已从 ORM 模型中移除，但 Schema 中仍保留。当前接口始终返回 `null`。建议同步清理 Schema。

---

### AiModelCap

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 能力记录 ID |
| cap_code | string | 是 | 能力编码，如 `json_output`、`tool_calls` |
| cap_name | string | 是 | 能力名称 |
| support_status | string | 是 | 支持状态：`supported` / `unsupported` / `beta` / `non_thinking_only` / `partial` |
| is_beta | bool | 是 | 是否 Beta |
| note | string \| null | 否 | 补充说明 |
| is_active | bool | 是 | 是否活跃（接口只返回 `true` 的记录） |
| created_at | datetime | 是 | 创建时间 |
| updated_at | datetime | 是 | 更新时间 |

---

### AiModelPrice

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 定价记录 ID |
| price_type | string | 是 | 价格类型，如 `input` / `output` / `cache_hit` |
| time_period | string | 是 | 时间周期，如 `peak` / `off_peak` |
| price | float | 是 | 价格（单位：元/百万 tokens） |
| created_at | datetime | 是 | 创建时间 |
| updated_at | datetime | 是 | 更新时间 |

---

## 已定义但未使用的 Schema

以下结构已在 `app/schema/detail.py` 中定义，暂无路由引用，供后续接口参考：

### ModelListResponse

| 字段 | 类型 | 说明 |
|------|------|------|
| items | AiModelBase[] | 模型列表 |
| total | int | 总记录数 |
| page | int | 当前页码 |
| page_size | int | 每页条数 |

### ProviderListResponse

| 字段 | 类型 | 说明 |
|------|------|------|
| items | AiProvider[] | 供应商列表 |
| total | int | 总记录数 |
| page | int | 当前页码 |
| page_size | int | 每页条数 |

### ProviderDetailResponse

| 字段 | 类型 | 说明 |
|------|------|------|
| provider | AiProvider | 供应商信息 |
| models | AiModelBase[] | 该供应商下的模型列表 |
