// ============================================================
// shared/types/display.ts
//
// 前后端共用的数据契约。所有字段与后端 schemas/ 下 to_xxx 函数的
// 返回值一一对应，均为原始返回，前端不做二次转换。
//
// 约定：
//   - 可空字段显式标注为 T | null，避免调用侧漏判空；
//   - 枚举值（thinking_support / support_status / price_type 等）
//     在展示层中文化，此处保留后端原始取值。
// ============================================================

/** 后端统一响应结构：code 为 200 表示业务成功 */
export interface ApiResponse<T> {
    msg: string;
    code: number;
    data: T;
}

// ---------------- 供应商 ----------------
/** 供应商实体，provider_code 为对外唯一标识（路由与接口均以它定位） */
export interface AiProvider {
    id: number;
    provider_code: string;
    provider_name: string;
    website_url: string | null;
    description: string | null;
    ico: string | null;
}

// ---------------- 模型 ----------------
/** 模型基础信息 */
export interface AiModelBase {
    id: number;
    model_slug: string;
    display_name: string;
    model_version: string | null;
    model_family: string | null;
    context_length_raw: string | null;
    max_output_raw: string | null;
    thinking_support: string;
    default_thinking_mode: string | null;
    thinking_note: string | null;
    concurrency_limit: number | null;
    doc_url: string | null;
    description: string | null;
    provider_id: number;
}

/**
 * 模型能力。
 * 注意：接口不返回 cap_code，展示与排序只能依赖 cap_name / support_status。
 */
export interface AiModelCap {
    id: number;
    cap_name: string;
    support_status: string;
    is_beta: boolean;
    note: string | null;
}

/** 模型定价，price 单位为「元 / 百万 tokens」 */
export interface AiModelPrice {
    id: number;
    price_type: string;
    time_period: string;
    price: number;
}

// ---------------- 接口返回体 ----------------
/** 模型详情：供应商 + 模型 + 能力列表 + 定价列表 */
export interface Detail {
    provider: AiProvider;
    model: AiModelBase;
    capabilities: AiModelCap[];
    prices: AiModelPrice[];
}

/**
 * 供应商列表项。
 * 列表接口直接返回 AiProvider 结构，因此以别名复用，不再单独定义。
 */
export type ProviderItem = AiProvider;

/**
 * 供应商概览：供应商详情 + 最近 5 条模型。
 * models_data 沿用后端字段名，未做重命名。
 */
export interface ProviderOverviewData {
    provider: AiProvider;
    models_data: AiModelBase[];
}
