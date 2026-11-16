# AIWiki 后端接口需求（前端提出）

> 提出方：前端　接收方：后端
> 版本：v1.0　日期：2026-11-16
> 说明：以下字段均基于**当前实测返回**提出，优先级已排序。前 3 项为 P0，直接决定首页信息密度。

---

## 〇、现状（实测）

| 接口 | 当前返回 |
|---|---|
| `GET /api/providers?page=&size=` | `{"msg":"返回信息","code":200,"data":[{id, provider_code, provider_name, website_url, description, ico}, …]}` |
| `GET /api/providers/{code}/overview` | `{"msg":"…","code":200,"data":{"provider":{…},"models_data":[ …最多 5 条… ]}}` |
| `GET /api/providers/{code}/models` | `{"msg":"…","code":200,"data":{"models_data":[ … ]}}` |
| `GET /api/models/{id}` | `{"msg":"…","code":200,"data":{"provider":{…},"model":{…},"capabilities":[…],"prices":[…]}}` |
| 不存在资源 | `HTTP 404` + `{"detail":"模型不存在或所属供应商已停用: id=999"}` |

**三个已确认的缺口**：列表无总数、列表项无聚合信息、错误响应结构与成功响应不一致。

---

## 一、P0-1　列表接口补充分页元信息

### 现状问题
`data` 只有数组，前端不知道总共有多少条，只能固定请求 `size=100`。
超过 100 条的部分**既不报错也不提示**，属于静默截断。

### 建议方案（**向后兼容，不改 data 结构**）

```http
GET /api/providers?page=1&size=12
```

```json
{
  "msg": "返回信息",
  "code": 200,
  "data": [ { "id": 1, "provider_code": "deepseek", "…": "…" } ],
  "total": 37,
  "page": 1,
  "size": 12
}
```

> **为什么不在 `data` 里再包一层 `{items,total}`**：
> `data` 目前是数组，其它调用方（含现有前端）都按数组消费。
> 改成对象属于**破坏性变更**。把 `total/page/size` 放在**顶层**即可兼容，
> 老调用方忽略新字段，一切照旧。

### 同样的改造请一并应用到
`GET /api/providers/{code}/models` —— 它目前返回 `data.models_data` 且无总数，
前端无法做"查看更多模型"。

### 前端用途
真实分页器 / "共 N 家" / "查看更多"。
同时消除测试报告中记录的 **RISK-002（超量数据静默截断）**。

---

## 二、P0-2　列表项增加聚合字段

### 现状问题
首页卡片目前只能显示 `provider_name` 与 `provider_code`，信息过薄。
若前端自行逐条请求 overview 补数据，就是典型的 **N+1 请求**。

### 建议方案（**纯新增，无破坏性**）

`GET /api/providers` 的每个 item 增加：

```json
{
  "id": 1,
  "provider_code": "deepseek",
  "provider_name": "DeepSeek",
  "website_url": "https://platform.deepseek.com/usage",
  "description": null,
  "ico": null,

  "model_count": 2,
  "min_price": 1.0,
  "max_context": "1M"
}
```

| 字段 | 类型 | 含义 | 为空的处理 |
|---|---|---|---|
| `model_count` | int | 该供应商已上架模型总数 | 无模型时返回 `0`（不要返回 null） |
| `min_price` | float \| null | 最低输入单价（元/百万 tokens） | 无价格记录时 `null` |
| `max_context` | string \| null | 最大上下文长度原始值，如 `"1M"` | 无记录时 `null` |

> ⚠️ **不要用 `models_data.length` 代替 `model_count`**：
> overview 只返回最近 5 条，供应商有 20 个模型时该值仍是 5，前端会显示错误数字。
> 这也是当前前端**刻意没有显示模型数**的原因——宁可不显示，也不显示错的。

### 前端用途
卡片显示「2 个模型 · 起价 ¥1.0 · 上下文 1M」，用户不必点进去即可横向比较。

---

## 三、P0-3　概览接口返回模型总数

### 现状问题
`GET /api/providers/{code}/overview` 的 `models_data` 固定最多 5 条，
无法区分「这个供应商只有 5 个模型」与「有 20 个但只显示 5 个」。
页面标题「模型列表 (最近 5 条)」因此不准确。

### 建议方案（**纯新增**）

```json
{
  "msg": "返回信息",
  "code": 200,
  "data": {
    "provider": { "…": "…" },
    "model_total": 2,
    "models_data": [ … ]
  }
}
```

### 前端用途
标题改为「模型列表（共 2 个，显示前 5）」，并在超过 5 个时显示「查看全部」入口。

---

## 四、P1-1　错误响应统一包装

### 现状问题
成功走 `{msg, code, data}`，失败走 FastAPI 默认 `{detail}`。
前端需要为错误分支写第二套解包逻辑；测试报告已记为 **RISK-004**。

### 建议方案（**兼容式：保留 detail，同时补包装**）

```json
// HTTP 404
{
  "msg": "模型不存在或所属供应商已停用",
  "code": 404,
  "data": null,
  "detail": "模型不存在或所属供应商已停用: id=999"
}
```

做法：注册全局异常处理器，在 `HTTPException` 响应中**追加** `msg/code/data`，
**保留** `detail`。这样现有依赖 `detail` 的调用方不受影响，前端可逐步切换。

HTTP 状态码保持语义（404 仍是 404，不要改成 200）。

---

## 五、P1-2　服务端搜索

### 现状问题
当前搜索是**前端在已加载的集合内过滤**。
若真有大量供应商，用户会搜不到未加载的数据——这是功能缺陷，不是性能问题。

### 建议方案（**纯新增参数**）

```http
GET /api/providers?keyword=deep&page=1&size=12
```

- 对 `provider_name` 做模糊匹配（可选同时匹配 `provider_code`）
- 大小写不敏感
- 返回结构与 P0-1 一致（含 `total`，且 `total` 应为**过滤后**的总数）

---

## 六、P2　模型详情附带同系列模型

### 建议方案（**纯新增**）

`GET /api/models/{id}` 的 `data` 增加：

```json
"siblings": [
  { "id": 2, "display_name": "DeepSeek-V4-Pro", "model_slug": "deepseek-v4-pro" }
]
```

### 前端用途
模型页底部加「同供应商其他模型」横条，提升浏览深度。

---

## 七、汇总

| 编号 | 接口 | 改动 | 破坏性 | 优先级 |
|---|---|---|---|---|
| 1 | `GET /api/providers` | 顶层增加 `total` / `page` / `size` | 否 | 🔴 P0 |
| 1b | `GET /api/providers/{code}/models` | 同上 | 否 | 🔴 P0 |
| 2 | `GET /api/providers` | item 增加 `model_count` / `min_price` / `max_context` | 否 | 🔴 P0 |
| 3 | `GET /api/providers/{code}/overview` | `data` 增加 `model_total` | 否 | 🔴 P0 |
| 4 | 全局 | 错误响应补 `msg/code/data`，保留 `detail` | 否 | 🟠 P1 |
| 5 | `GET /api/providers` | 新增 `keyword` 查询参数 | 否 | 🟠 P1 |
| 6 | `GET /api/models/{id}` | `data` 增加 `siblings[]` | 否 | 🟡 P2 |

**全部 7 项均为向后兼容改动，不修改任何现有字段的类型或结构。**

### 如果只能做一件事
做 **1 + 2**。这两项到位后，首页卡片才能从「只有一个名字」变成
「名字 + 模型数 + 起价 + 上下文」，信息密度会有质的变化。

---

## 八、联调约定

1. **字段名可以调整**，定稿后同步给前端即可（前端按实际字段接入，成本很低）。
2. 建议先在 `feat/frontend-init` 分支对应的本地环境验证，前端会用 curl 断言复核。
3. 若某项暂不实现，请告知，前端会保留降级显示（当前所有新字段都做了空值兜底）。
