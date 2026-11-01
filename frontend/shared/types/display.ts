// ============================================================
// shared/types/display.ts
// ============================================================

export interface ApiResponse<T> {
    msg: string;
    code: number;
    data: T;
}

// ---------------- 供应商类型 ----------------
export interface AiProvider {
    id: number;
    provider_code: string;
    provider_name: string;
    website_url: string | null;
    description: string | null;
    ico: string | null;
}

// ---------------- 模型相关类型 ----------------
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

export interface AiModelCap {
    id: number;
    cap_name: string;
    support_status: string;
    is_beta: boolean;
    note: string | null;
}

export interface AiModelPrice {
    id: number;
    price_type: string;
    time_period: string;
    price: number;
}

export interface Detail {
    provider: AiProvider;
    model: AiModelBase;
    capabilities: AiModelCap[];
    prices: AiModelPrice[];
}

// ---------------- 列表与概览类型 ----------------

// 首页列表返回的就是 AiProvider，不需要再单独定义 ProviderItem 了
export type ProviderItem = AiProvider;

// 供应商页概览的返回结构
export interface ProviderOverviewData {
    provider: AiProvider;
    models_data: AiModelBase[];
}