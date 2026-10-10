-- ============================================================
-- base.sql — 由 ORM 模型生成的基线 DDL
-- 基于 app/model/ 下的 SQLAlchemy 模型定义
-- 数据库: MySQL 8+  字符集: utf8mb4
-- 生成日期: 2026-10-10
-- ============================================================

-- ------------------------------------------------------------
-- 1. ai_provider — 模型供应商
-- ORM: app/model/provider.py → Provider
-- ------------------------------------------------------------
CREATE TABLE `ai_provider` (
    `id`            INT          NOT NULL AUTO_INCREMENT,
    `provider_code` VARCHAR(50)     NOT NULL                COMMENT '供应商标识，如 deepseek',
    `provider_name` VARCHAR(100)    NOT NULL                COMMENT '供应商名称，如 DeepSeek',
    `website_url`   VARCHAR(255)    DEFAULT NULL            COMMENT '官网/文档地址',
    `status`        INT             NOT NULL DEFAULT 1      COMMENT '1启用 0停用',
    `created_at`    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_provider_code` (`provider_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='模型供应商';


-- ------------------------------------------------------------
-- 2. ai_model — AI 模型
-- ORM: app/model/aimodel.py → Ai_Model
-- ------------------------------------------------------------
CREATE TABLE `ai_model` (
    `id`                    INT          NOT NULL AUTO_INCREMENT,
    `model_slug`            VARCHAR(100)    NOT NULL                COMMENT '模型标识/列名',
    `display_name`          VARCHAR(150)    NOT NULL                COMMENT '展示名',
    `model_version`         VARCHAR(100)    DEFAULT NULL            COMMENT '模型版本',
    `model_family`          VARCHAR(100)    DEFAULT NULL            COMMENT '模型系列',

    -- 上下文长度
    `context_length_raw`    VARCHAR(32)     DEFAULT NULL            COMMENT '上下文长度原文，如 1M',

    -- 最大输出
    `max_output_raw`        VARCHAR(32)     DEFAULT NULL            COMMENT '最大输出原文，如 最大 384K',

    -- 思考模式
    `thinking_support`      VARCHAR(32)     NOT NULL DEFAULT 'unknown' COMMENT '思考模式支持: none/non_thinking_only/thinking_only/both/unknown',
    `default_thinking_mode` VARCHAR(32)     DEFAULT NULL            COMMENT '默认模式：non_thinking/thinking/unknown',
    `thinking_note`         VARCHAR(255)    DEFAULT NULL            COMMENT '思考模式切换说明',

    -- 限制与状态
    `concurrency_limit`     INT             DEFAULT NULL            COMMENT '并发限制',
    `status`                VARCHAR(20)     NOT NULL DEFAULT 'active' COMMENT 'active/inactive/deprecated',

    -- 文档与备注
    `doc_url`               VARCHAR(255)    DEFAULT NULL            COMMENT '模型文档地址',
    `description`           TEXT            DEFAULT NULL            COMMENT '模型描述',

    -- 外键
    `provider_id`           INT          NOT NULL                COMMENT '供应商ID',

    -- 时间戳
    `created_at`            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_provider_slug` (`provider_id`, `model_slug`),
    CONSTRAINT `fk_model_provider` FOREIGN KEY (`provider_id`) REFERENCES `ai_provider` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI 模型';


-- ------------------------------------------------------------
-- 3. ai_model_cap — 模型能力
-- ORM: app/model/aimodelcap.py → Ai_Model_Cap
-- ------------------------------------------------------------
CREATE TABLE `ai_model_cap` (
    `id`                INT          NOT NULL AUTO_INCREMENT,
    `cap_code`          VARCHAR(64)     NOT NULL                COMMENT '能力编码',
    `cap_name`          VARCHAR(100)    NOT NULL                COMMENT '能力名称',
    `support_status`    VARCHAR(32)     NOT NULL                COMMENT 'supported/unsupported/beta/non_thinking_only/partial',
    `is_beta`           TINYINT(1)      NOT NULL DEFAULT 0      COMMENT '是否 Beta',
    `note`              VARCHAR(255)    DEFAULT NULL            COMMENT '补充说明',

    -- 外键
    `model_id`          INT          NOT NULL                COMMENT '模型ID',

    -- 时间戳
    `created_at`        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_active`         TINYINT(1)      NOT NULL DEFAULT 1,

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_model_cap` (`model_id`, `cap_code`),
    CONSTRAINT `fk_cap_model` FOREIGN KEY (`model_id`) REFERENCES `ai_model` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='模型能力';


-- ------------------------------------------------------------
-- 4. ai_model_price — 模型定价
-- ORM: app/model/aimodelprice.py → Ai_Model_Price
-- ------------------------------------------------------------
CREATE TABLE `ai_model_price` (
    `id`            INT             NOT NULL AUTO_INCREMENT,
    `model_id`      INT             NOT NULL                COMMENT '模型ID',
    `price_type`    VARCHAR(255)    NOT NULL                COMMENT '价格类型',
    `price`         DECIMAL(12, 4)  NOT NULL                COMMENT '价格',
    `time_period`   VARCHAR(255)    DEFAULT NULL            COMMENT '时间周期',

    -- 时间戳
    `created_at`    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`),
    CONSTRAINT `fk_price_model` FOREIGN KEY (`model_id`) REFERENCES `ai_model` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='模型定价';
