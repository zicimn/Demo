// ============================================================
// shared/types/display.ts (基于后端最新重构更新)
// ============================================================

// 统一的 API 响应结构
export interface ApiResponse<T> {
    msg: string;
    code: number;
    data: T;
}

// ---------------- 详情页相关类型 ----------------

export interface Detail {
    provider: AiProvider;
    model: AiModelBase;
    capabilities: AiModelCap[];
    prices: AiModelPrice[];
}

export interface AiProvider {
    id: number;
    provider_code: string;
    provider_name: string;
    website_url: string | null;
}

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

// ---------------- 首页列表相关类型 ----------------

export interface ProviderItem {
    id: number;
    name: string;
    ico: string | null;
}