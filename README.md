# AIWiki · AI 模型信息百科平台

> 按供应商浏览 AI 模型的**能力、上下文长度、并发限制与定价**，一个前后端分离的速查站点。

---

## 项目简介

AIWiki 面向"模型太多、参数太散、定价太乱"的现实问题：同一个厂商下有多代模型，能力、上下文、峰值/低谷价格各不相同，官方文档分散在各处。本项目把这类信息结构化，提供统一的检索入口。

- **前端**：Nuxt 4 + Vue 3 + TypeScript，服务端渲染（SSR）
- **后端**：FastAPI + SQLAlchemy 2.0（异步）
- **数据库**：MySQL 8（utf8mb4）

---

## 功能特性

### 已完成

| 模块 | 说明 |
|---|---|
| 供应商列表 | 卡片网格展示所有启用中的供应商；无图标时回退为名称首字母圆形头像；图片加载失败同样回退 |
| 本地实时搜索 | 基于 `computed` 依赖追踪过滤，大小写不敏感、支持一键清除、纯空格不触发过滤 |
| 供应商详情 | 展示名称、标识、官网、简介，以及该供应商最近 5 条模型 |
| 模型详情 | 供应商信息、模型基础参数、支持能力、定价表四块；枚举值统一中文化 |
| 状态兜底 | 加载中 / 空数据 / 404 / 网络断开 四类场景分别渲染，并提供重试 |
| 异常归因 | 区分「后端未启动」与「真实 HTTP 500」——Nuxt 会将二者统一包装为 status 500，仅看状态码无法分辨 |
| 体验细节 | 全局顶部进度条、页面切换淡入淡出、吸顶导航、响应式布局 |

### 规划中

- 供应商侧分页与关键词检索（当前由前端本地过滤）
- 模型收藏与对比
- 定价历史变更记录

---

## 技术栈

**前端**

| 分类 | 选型 |
|---|---|
| 框架 | Nuxt 4 / Vue 3（Composition API） |
| 语言 | TypeScript |
| 渲染 | SSR（服务端渲染） |
| 样式 | 原生 CSS（Flex / Grid / 响应式断点），无 UI 组件库 |

**后端**

| 分类 | 选型 |
|---|---|
| 框架 | FastAPI |
| ORM | SQLAlchemy 2.0（async）+ aiomysql |
| 数据库 | MySQL 8 |
| 缓存 | Redis（惰性连接，当前接口未强依赖） |

---

## 目录结构

```
Demo/
├─ app/                      # 后端（app/ 是导入根，不是包）
│  ├─ api/                   # 路由层：provider.py / model.py
│  ├─ services/              # 业务层
│  ├─ schemas/               # 响应体组装（to_xxx 纯函数）
│  ├─ models/                # ORM 模型
│  ├─ config/                # 数据库、缓存、环境变量
│  ├─ utils/                 # 统一响应与业务异常
│  ├─ deps.py                # 依赖注入
│  └─ main.py                # 应用入口、CORS、异常兜底
├─ frontend/                 # 前端（Nuxt 4，srcDir 为 app/）
│  ├─ app/
│  │  ├─ app.vue             # 根组件（NuxtLayout 挂载点）
│  │  ├─ layouts/            # 全局布局
│  │  ├─ pages/              # 文件路由
│  │  ├─ components/         # 业务组件
│  │  ├─ composables/        # 组合式函数
│  │  └─ assets/css/         # 全局样式
│  ├─ shared/types/          # 前后端共用的类型定义
│  └─ nuxt.config.ts
├─ sql/                      # 建表与种子数据
└─ requirements.txt
```

---

## 快速开始

### 1. 数据库

```sql
CREATE DATABASE aiwiki DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

依次执行 `sql/base.sql`（建表）与 `sql/data.sql`（种子数据）。

### 2. 后端

```bash
# 创建并激活虚拟环境
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# 安装依赖
pip install -r requirements.txt
```

在 `app/.env` 中配置数据库连接（**该文件不入库，请勿提交**）：

```
ASYNC_DATABASE_URL=mysql+aiomysql://<user>:<password>@localhost:3306/aiwiki?charset=utf8mb4
```

启动：

```bash
uvicorn main:app --app-dir app --reload --port 8000
```

> `app/` 是导入根，因此必须带 `--app-dir app`，否则会 `ModuleNotFoundError`。

### 3. 前端

```bash
cd frontend
npm install
npm run dev
```

打开 http://localhost:3000 。后端默认监听 8000 端口。

如需切换接口地址，用环境变量覆盖，不改代码：

```bash
set NUXT_PUBLIC_API_BASE=http://localhost:8000/api   # Windows cmd
# export NUXT_PUBLIC_API_BASE=...                    # macOS / Linux
```

---

## API 接口

统一响应结构：

```json
{ "msg": "返回信息", "code": 200, "data": {} }
```

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/providers` | 供应商分页列表（`page` / `size`，size 上限 100） |
| GET | `/api/providers/{provider_code}` | 供应商详情 |
| GET | `/api/providers/{provider_code}/models` | 该供应商的模型分页列表 |
| GET | `/api/providers/{provider_code}/overview` | 供应商详情 + 最近 5 条模型（供应商页使用） |
| GET | `/api/models/{id}` | 模型详情（含供应商、能力、定价） |

**约定**

- 列表接口查无数据时返回 `404`，`data` 不返回空数组；前端按"无数据"处理而非报错
- 供应商详情以 `provider_code` 定位，不是自增 `id`
- `capabilities` 不返回 `cap_code`；`prices.time_period` 存在 `peak` / `off_peak` / `standard` 三种取值

交互式文档：http://localhost:8000/docs

---

## 环境变量

| 变量 | 归属 | 说明 |
|---|---|---|
| `ASYNC_DATABASE_URL` | 后端 | 数据库连接串，位于 `app/.env`（不入库） |
| `CORS_ORIGINS` | 后端 | 允许的前端源，默认 `http://localhost:3000` |
| `NUXT_PUBLIC_API_BASE` | 前端 | 接口基础地址，默认 `http://localhost:8000/api` |

> ⚠️ 浏览器端请求受 CORS 限制：请用 `http://localhost:3000` 访问，`http://127.0.0.1:3000` 会被后端拒绝。

---

## 开发约定

- **后端导入**：以 `app/` 为根使用绝对导入（`from services.provider import ...`），不使用 `..` 相对导入
- **前端别名**：跨层类型统一从 `#shared/types/display` 导入
- **提交规范**：`feat:` / `fix:` / `refactor:` / `chore:` + 简短中文说明
- **协作流程**：Fork → Feature 分支 → Pull Request → 合并到 `main`

---

## 数据库设计

四张核心表，围绕「供应商 → 模型 → 能力 / 定价」展开：

| 表 | 说明 |
|---|---|
| `ai_provider` | 供应商，`provider_code` 唯一；`status` 控制是否对外展示 |
| `ai_model` | 模型，含上下文长度、最大输出、思考模式、并发限制 |
| `ai_model_cap` | 模型能力（`json_output`、`tool_calls` 等），`is_active` 控制是否展示 |
| `ai_model_price` | 定价，按 `price_type`（输入/输出/缓存）与 `time_period`（峰谷）分段 |

`sql/base.sql` 为建表脚本，`sql/data.sql` 为示例数据。以实际数据库结构为准。

---

## 许可

本项目为学习实践项目，未附带开源许可。
