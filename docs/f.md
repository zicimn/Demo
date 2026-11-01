# 前端接口变更说明

> 后端已将 `/api/home/*` 与 `/api/models/*` 两套路由合并为资源化路由，并统一了供应商数据结构。
> 本文档面向前端，列出**旧接口 → 新接口**的对应关系、请求参数、响应结构以及必须修改的地方。
>
> 变更日期：2026-10-30

---

## 一、接口变更总览

| 功能 | 旧接口（已删除） | 新接口 |
|---|---|---|
| 供应商列表 | `GET /api/home/` | `GET /api/providers` |
| 供应商详情 | 无独立接口（原本内嵌在首页接口里） | `GET /api/providers/{provider_code}` |
| 某供应商的模型列表 | `GET /api/models/{provider_code}` | `GET /api/providers/{provider_code}/models` |
| 首页概览（供应商 + 最近 5 条模型） | `GET /api/home/models/{provider_code}` | `GET /api/providers/{provider_code}/overview` |
| 模型详情 | `GET /api/models/?id={id}` | `GET /api/models/{model_id}` |

旧路由 `/api/home/*` 已经不存在，继续请求会得到 404，请全部替换。

---

## 二、通用约定

### 2.1 成功响应

所有接口成功时 HTTP 状态码为 `200`，响应体统一为：

```json
{
  "msg": "返回信息",
  "code": 200,
  "data": { }
}
```

列表类接口的 `data` 是数组或包含 `models_data` 的对象，详见各接口说明。

### 2.2 错误响应

业务错误（供应商/模型不存在或已停用、分页超出范围）由后端转成标准 HTTP 错误：

```json
{
  "detail": "供应商不存在或已停用: provider_code=xxx"
}
```

注意：

- **错误响应没有 `msg` / `code` 包裹**，只有 `detail`，请以 HTTP 状态码为准。
- 404：资源不存在或已停用。
- 422：参数校验失败（例如把字符串塞进了要求 `int` 的 `model_id`）。

### 2.3 分页

- `page` 从 **1** 开始，`size` 取值范围 `1 ~ 100`。
- **供应商列表**分页超出数据范围时（比如只有 2 条却请求 `page=5`）返回 **404**，前端翻页时要处理这种情况；**模型列表**越界则返回 `models_data: []`（空数组），不报错。
- 供应商列表 `size` 默认 `20`；模型列表 `size` 默认 `10`。

### 2.4 状态过滤

- 供应商 `status = 0`（停用）时，其详情、模型列表、概览一律返回 **404**，前端无需再自行过滤。
- 模型只返回 `status = "active"` 的记录。

---

## 三、接口详情

### 3.1 供应商列表

```http
GET /api/providers?page=1&size=20
```

| 参数 | 位置 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| `page` | query | int | 否 | 1 | 页码，从 1 开始 |
| `size` | query | int | 否 | 20 | 每页条数，1~100 |

响应示例：

```json
{
  "msg": "返回信息",
  "code": 200,
  "data": [
    {
      "id": 1,
      "provider_code": "deepseek",
      "provider_name": "DeepSeek",
      "website_url": "https://api.deepseek.com",
      "description": null,
      "ico": null
    },
    {
      "id": 2,
      "provider_code": "moonshot",
      "provider_name": "Moonshot AI (Kimi)",
      "website_url": "https://platform.moonshot.cn/",
      "description": null,
      "ico": null
    }
  ]
}
```

> **注意**：旧版本列表项里的 `name` 字段已改名为 `provider_name`，并新增 `website_url`、`description`、`ico`。

### 3.2 供应商详情

```http
GET /api/providers/{provider_code}
```

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `provider_code` | path | string | 是 | 供应商标识，如 `deepseek` |

响应示例（`data` 为单个对象）：

```json
{
  "msg": "返回信息",
  "code": 200,
  "data": {
    "id": 1,
    "provider_code": "deepseek",
    "provider_name": "DeepSeek",
    "website_url": "https://api.deepseek.com",
    "description": null,
    "ico": null
  }
}
```

### 3.3 某供应商的模型列表

```http
GET /api/providers/{provider_code}/models?page=1&size=10
```

| 参数 | 位置 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| `provider_code` | path | string | 是 | - | 供应商标识 |
| `page` | query | int | 否 | 1 | 页码 |
| `size` | query | int | 否 | 10 | 每页条数，1~100 |

响应示例：

```json
{
  "msg": "返回信息",
  "code": 200,
  "data": {
    "models_data": [
      {
        "id": 1,
        "model_slug": "deepseek-flash",
        "display_name": "DeepSeek-V4.1-Flash",
        "model_version": "DeepSeek-V4.1-Flash",
        "model_family": "DeepSeek-V4",
        "context_length_raw": "1M",
        "max_output_raw": "最大 384K",
        "thinking_support": "both",
        "default_thinking_mode": "thinking",
        "thinking_note": "切换方式详见思考模式",
        "concurrency_limit": 2500,
        "doc_url": "https://api.deepseek.com",
        "description": "DeepSeek-V4.1-Flash，支持思考模式，支持图像理解",
        "provider_id": 1
      }
    ]
  }
}
```

> 模型列表字段与旧接口完全一致，只是 URL 变了。

### 3.4 首页概览（供应商 + 最近 5 条模型）

```http
GET /api/providers/{provider_code}/overview
```

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `provider_code` | path | string | 是 | 供应商标识 |

固定返回该供应商最近 5 条模型（按 `publish_at` 倒序），不分页。

响应示例：

```json
{
  "msg": "返回信息",
  "code": 200,
  "data": {
    "provider": {
      "id": 1,
      "provider_code": "deepseek",
      "provider_name": "DeepSeek",
      "website_url": "https://api.deepseek.com",
      "description": null,
      "ico": null
    },
    "models_data": [
      {
        "id": 1,
        "model_slug": "deepseek-flash",
        "display_name": "DeepSeek-V4.1-Flash",
        "thinking_support": "both",
        "context_length_raw": "1M",
        "max_output_raw": "最大 384K",
        "provider_id": 1
      }
    ]
  }
}
```

> **注意结构变化**：
> - 旧字段 `provider_data` 改名为 `provider`；
> - `provider` 直接是供应商对象，不再套一层 `{msg, code, data}`；
> - 前端取值从 `res.data.provider_data.data.xxx`（旧）改为 `res.data.provider.xxx`（新）；
> - 模型列表仍是 `res.data.models_data`。
>
> 该接口的模型数据与 `/api/providers/{provider_code}/models` 的前 5 条重叠，首页只需调这一个接口即可，不需要再额外请求模型列表。

### 3.5 模型详情

```http
GET /api/models/{model_id}
```

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `model_id` | path | int | 是 | 模型 id，**不再是 query 参数** |

响应示例：

```json
{
  "msg": "返回信息",
  "code": 200,
  "data": {
    "provider": {
      "id": 1,
      "provider_code": "deepseek",
      "provider_name": "DeepSeek",
      "website_url": "https://api.deepseek.com",
      "description": null,
      "ico": null
    },
    "model": {
      "id": 1,
      "model_slug": "deepseek-flash",
      "display_name": "DeepSeek-V4.1-Flash",
      "model_version": "DeepSeek-V4.1-Flash",
      "model_family": "DeepSeek-V4",
      "context_length_raw": "1M",
      "max_output_raw": "最大 384K",
      "thinking_support": "both",
      "default_thinking_mode": "thinking",
      "thinking_note": "切换方式详见思考模式",
      "concurrency_limit": 2500,
      "doc_url": "https://api.deepseek.com",
      "description": "DeepSeek-V4.1-Flash，支持思考模式，支持图像理解",
      "provider_id": 1
    },
    "capabilities": [
      {
        "id": 1,
        "cap_name": "Json Output",
        "support_status": "supported",
        "is_beta": false,
        "note": null
      },
      {
        "id": 2,
        "cap_name": "Tool Calls",
        "support_status": "supported",
        "is_beta": false,
        "note": null
      }
    ],
    "prices": [
      {
        "id": 1,
        "price_type": "缓存名中",
        "time_period": "非高峰时期",
        "price": 0.02
      },
      {
        "id": 5,
        "price_type": "输出",
        "time_period": "非高峰时期",
        "price": 4.0
      }
    ]
  }
}
```

> `price` 为**数字**（最多 4 位小数），不是字符串，可直接参与计算/格式化。
> `provider` 对象与列表、详情接口保持同一形状（旧版本模型详情里的 provider 少了 `description` 和 `ico`，现在已补全）。
>
> `price_type` / `time_period` 是后端配置的展示文案（如 `输入`、`输出`、`缓存名中`、`高峰时期`、`非高峰时期`），当前种子数据里缓存相关文案存在错别字（`缓存名中`、`缓存未名中`），联调时以接口实际返回为准，前端**不要用文案做逻辑判断**。

---

## 四、字段字典

### 4.1 供应商（Provider）

| 字段 | 类型 | 可能为 null | 说明 |
|---|---|---|---|
| `id` | int | 否 | 供应商 id |
| `provider_code` | string | 否 | 供应商标识，如 `deepseek`，用于 URL |
| `provider_name` | string | 否 | 展示名，如 `DeepSeek` |
| `website_url` | string | 是 | 官网/文档地址 |
| `description` | string | 是 | 厂商介绍 |
| `ico` | string | 是 | 图标地址 |

### 4.2 模型（Model）

| 字段 | 类型 | 可能为 null | 说明 |
|---|---|---|---|
| `id` | int | 否 | 模型 id |
| `model_slug` | string | 否 | 模型标识 |
| `display_name` | string | 否 | 展示名 |
| `model_version` | string | 是 | 模型版本 |
| `model_family` | string | 是 | 模型系列 |
| `context_length_raw` | string | 是 | 上下文长度原文，如 `1M` |
| `max_output_raw` | string | 是 | 最大输出原文，如 `最大 384K` |
| `thinking_support` | string | 否 | 思考模式支持，见 4.4 |
| `default_thinking_mode` | string | 是 | 默认模式 |
| `thinking_note` | string | 是 | 思考模式说明 |
| `concurrency_limit` | int | 是 | 并发限制 |
| `doc_url` | string | 是 | 文档地址 |
| `description` | string | 是 | 模型描述 |
| `provider_id` | int | 否 | 所属供应商 id |

### 4.3 能力（Capability）

| 字段 | 类型 | 可能为 null | 说明 |
|---|---|---|---|
| `id` | int | 否 | 能力 id |
| `cap_name` | string | 否 | 能力名称，如 `Tool Calls` |
| `support_status` | string | 否 | 支持状态，见 4.4 |
| `is_beta` | bool | 否 | 是否 Beta |
| `note` | string | 是 | 补充说明 |

### 4.4 枚举值

`thinking_support`：

| 值 | 含义 |
|---|---|
| `none` | 不支持思考模式 |
| `non_thinking_only` | 仅非思考模式 |
| `thinking_only` | 仅思考模式 |
| `both` | 两种模式都支持 |
| `unknown` | 未知 |

`support_status`（能力支持状态）：

| 值 | 含义 |
|---|---|
| `supported` | 支持 |
| `unsupported` | 不支持 |
| `beta` | Beta 支持 |
| `non_thinking_only` | 仅非思考模式支持 |
| `partial` | 部分支持 |

---

## 五、前端修改清单

- [ ] 把 `/api/home/` 改为 `/api/providers`
- [ ] 把 `/api/home/models/{code}` 改为 `/api/providers/{code}/overview`
- [ ] 把 `/api/models/{code}`（模型列表）改为 `/api/providers/{code}/models`
- [ ] 把 `/api/models/?id={id}`（模型详情）改为 `/api/models/{id}`
- [ ] 供应商列表项字段 `name` 改为 `provider_name`
- [ ] 供应商结构统一后，列表/详情/模型详情里的 provider 都可以用同一套字段解析（新增 `website_url`、`description`、`ico`）
- [ ] overview 里 `provider_data` 改为 `provider`，去掉多余的 `.data` 层级
- [ ] 错误处理改为按 HTTP 状态码判断（404 / 422），错误信息读 `detail` 字段
- [ ] 分页越界返回 404，翻页逻辑需要兜底

---

## 六、联调自测

```bash
# 供应商列表
curl http://localhost:8000/api/providers?page=1&size=20

# 供应商详情
curl http://localhost:8000/api/providers/deepseek

# 供应商模型列表
curl "http://localhost:8000/api/providers/deepseek/models?page=1&size=10"

# 首页概览
curl http://localhost:8000/api/providers/deepseek/overview

# 模型详情
curl http://localhost:8000/api/models/1

# 预期 404：不存在的供应商
curl -i http://localhost:8000/api/providers/not-exist

# 预期 422：模型 id 传了非数字
curl -i http://localhost:8000/api/models/deepseek
```

浏览器直接打开 `http://localhost:8000/docs` 可以看到最新的接口文档。

---

## 七、常见问题

1. **`/api/providers` 带尾斜杠会怎样？**
   会 307 重定向到 `/api/providers`，建议直接使用不带尾斜杠的地址。

2. **`/api/models/deepseek` 为什么不是模型列表了？**
   模型列表已经移到 `/api/providers/{provider_code}/models`。`/api/models/{model_id}` 只接受数字 id，传字符串会得到 422。

3. **供应商详情和 overview 有什么区别？**
   - 详情只返回供应商信息，不查模型，适合只展示厂商信息的页面；
   - overview 额外返回最近 5 条模型，适合首页这类需要一次拿全的场景。

4. **模型列表里 `provider_id` 有什么用？**
   用于跳转模型详情（`/api/models/{id}` 用的是模型 `id`，不是 `model_slug`）。