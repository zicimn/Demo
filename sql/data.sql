/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80034 (8.0.34)
 Source Host           : localhost:3306
 Source Schema         : web2

 Target Server Type    : MySQL
 Target Server Version : 80034 (8.0.34)
 File Encoding         : 65001

 Date: 15/10/2026 09:08:39
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Records of ai_model
-- ----------------------------
INSERT INTO `ai_model` VALUES (1, 'deepseek-flash', 'DeepSeek-V4.1-Flash', 'DeepSeek-V4.1-Flash', 'DeepSeek-V4', '1M', '最大 384K', 'both', 'thinking', '切换方式详见思考模式', 2500, 'active', 'https://api.deepseek.com', 'DeepSeek-V4.1-Flash，支持思考模式，支持图像理解', 1, '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model` VALUES (2, 'deepseek-v4-pro', 'DeepSeek-V4-Pro', 'DeepSeek-V4-Pro-0813', 'DeepSeek-V4', '1M', '最大 384K', 'both', 'thinking', '切换方式详见思考模式', 500, 'active', 'https://api.deepseek.com', 'DeepSeek-V4-Pro-0813，支持思考模式，不支持图像理解', 1, '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model` VALUES (3, 'moonshot-v1-8k', 'Moonshot v1 8K', 'moonshot-v1-8k', 'Moonshot', '8K', '8K', 'none', 'non_thinking', '不支持思考模式', NULL, 'active', 'https://platform.moonshot.cn/docs', 'Moonshot v1 8K，适合短文本任务', 2, '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model` VALUES (4, 'moonshot-v1-32k', 'Moonshot v1 32K', 'moonshot-v1-32k', 'Moonshot', '32K', '32K', 'none', 'non_thinking', '不支持思考模式', NULL, 'active', 'https://platform.moonshot.cn/docs', 'Moonshot v1 32K，适合中等长度文本', 2, '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model` VALUES (5, 'moonshot-v1-128k', 'Moonshot v1 128K', 'moonshot-v1-128k', 'Moonshot', '128K', '128K', 'none', 'non_thinking', '不支持思考模式', NULL, 'active', 'https://platform.moonshot.cn/docs', 'Moonshot v1 128K，适合长文本', 2, '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model` VALUES (6, 'kimi-k2-0711-preview', 'Kimi K2 Preview', 'kimi-k2-0711-preview', 'Kimi K2', '128K', '128K', 'both', 'non_thinking', '支持思考模式，可通过参数切换', NULL, 'active', 'https://platform.moonshot.cn/docs', 'Kimi K2 预览版，支持工具调用与思考模式', 2, '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model` VALUES (7, 'qwen-max', 'Qwen-Max', 'qwen-max', 'Qwen', '32K', '8K', 'none', 'non_thinking', '不支持思考模式', NULL, 'active', 'https://help.aliyun.com/zh/dashscope/', '通义千问 Max，适合复杂任务', 3, '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model` VALUES (8, 'qwen-plus', 'Qwen-Plus', 'qwen-plus', 'Qwen', '128K', '8K', 'none', 'non_thinking', '不支持思考模式', NULL, 'active', 'https://help.aliyun.com/zh/dashscope/', '通义千问 Plus，平衡性能与成本', 3, '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model` VALUES (9, 'qwen-turbo', 'Qwen-Turbo', 'qwen-turbo', 'Qwen', '1M', '8K', 'none', 'non_thinking', '不支持思考模式', NULL, 'active', 'https://help.aliyun.com/zh/dashscope/', '通义千问 Turbo，高速低成本', 3, '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model` VALUES (10, 'qwen3-235b-a22b', 'Qwen3 235B A22B', 'qwen3-235b-a22b', 'Qwen3', '128K', '32K', 'both', 'thinking', '支持思考模式，默认开启', NULL, 'active', 'https://help.aliyun.com/zh/dashscope/', 'Qwen3 大模型，支持思考模式', 3, '2026-10-10 18:09:14', '2026-10-10 18:09:14');


-- ----------------------------
-- Records of ai_model_cap
-- ----------------------------
INSERT INTO `ai_model_cap` VALUES (1, 'json_output', 'Json Output', 'supported', 0, NULL, 1, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (2, 'tool_calls', 'Tool Calls', 'supported', 0, NULL, 1, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (3, 'responses_api', 'Responses API', 'supported', 0, NULL, 1, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (4, 'anthropic_api', 'Anthropic API', 'supported', 0, NULL, 1, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (5, 'dialogue_prefix_continuation', '对话前缀续写', 'supported', 1, 'Beta', 1, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (6, 'fim_completion', 'FIM 补全', 'non_thinking_only', 1, 'Beta；仅非思考模式支持', 1, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (7, 'image_understanding', '图像理解', 'supported', 0, NULL, 1, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (8, 'json_output', 'Json Output', 'supported', 0, NULL, 2, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (9, 'tool_calls', 'Tool Calls', 'supported', 0, NULL, 2, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (10, 'responses_api', 'Responses API', 'supported', 0, NULL, 2, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (11, 'anthropic_api', 'Anthropic API', 'supported', 0, NULL, 2, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (12, 'dialogue_prefix_continuation', '对话前缀续写', 'supported', 1, 'Beta', 2, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (13, 'fim_completion', 'FIM 补全', 'non_thinking_only', 1, 'Beta；仅非思考模式支持', 2, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (14, 'image_understanding', '图像理解', 'unsupported', 0, NULL, 2, '2026-10-10 18:03:39', '2026-10-10 18:03:39', 1);
INSERT INTO `ai_model_cap` VALUES (15, 'json_output', 'Json Output', 'supported', 0, NULL, 3, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (16, 'tool_calls', 'Tool Calls', 'supported', 0, NULL, 3, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (17, 'responses_api', 'Responses API', 'unsupported', 0, NULL, 3, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (18, 'anthropic_api', 'Anthropic API', 'unsupported', 0, NULL, 3, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (19, 'image_understanding', '图像理解', 'unsupported', 0, NULL, 3, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (20, 'json_output', 'Json Output', 'supported', 0, NULL, 4, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (21, 'tool_calls', 'Tool Calls', 'supported', 0, NULL, 4, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (22, 'responses_api', 'Responses API', 'unsupported', 0, NULL, 4, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (23, 'anthropic_api', 'Anthropic API', 'unsupported', 0, NULL, 4, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (24, 'image_understanding', '图像理解', 'unsupported', 0, NULL, 4, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (25, 'json_output', 'Json Output', 'supported', 0, NULL, 5, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (26, 'tool_calls', 'Tool Calls', 'supported', 0, NULL, 5, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (27, 'responses_api', 'Responses API', 'unsupported', 0, NULL, 5, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (28, 'anthropic_api', 'Anthropic API', 'unsupported', 0, NULL, 5, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (29, 'image_understanding', '图像理解', 'unsupported', 0, NULL, 5, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (30, 'json_output', 'Json Output', 'supported', 0, NULL, 6, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (31, 'tool_calls', 'Tool Calls', 'supported', 0, NULL, 6, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (32, 'responses_api', 'Responses API', 'supported', 0, NULL, 6, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (33, 'anthropic_api', 'Anthropic API', 'unsupported', 0, NULL, 6, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (34, 'image_understanding', '图像理解', 'unsupported', 0, NULL, 6, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (35, 'json_output', 'Json Output', 'supported', 0, NULL, 7, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (36, 'tool_calls', 'Tool Calls', 'supported', 0, NULL, 7, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (37, 'responses_api', 'Responses API', 'supported', 0, NULL, 7, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (38, 'anthropic_api', 'Anthropic API', 'unsupported', 0, NULL, 7, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (39, 'image_understanding', '图像理解', 'unsupported', 0, NULL, 7, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (40, 'json_output', 'Json Output', 'supported', 0, NULL, 8, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (41, 'tool_calls', 'Tool Calls', 'supported', 0, NULL, 8, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (42, 'responses_api', 'Responses API', 'supported', 0, NULL, 8, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (43, 'anthropic_api', 'Anthropic API', 'unsupported', 0, NULL, 8, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (44, 'image_understanding', '图像理解', 'unsupported', 0, NULL, 8, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (45, 'json_output', 'Json Output', 'supported', 0, NULL, 9, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (46, 'tool_calls', 'Tool Calls', 'supported', 0, NULL, 9, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (47, 'responses_api', 'Responses API', 'supported', 0, NULL, 9, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (48, 'anthropic_api', 'Anthropic API', 'unsupported', 0, NULL, 9, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (49, 'image_understanding', '图像理解', 'unsupported', 0, NULL, 9, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (50, 'json_output', 'Json Output', 'supported', 0, NULL, 10, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (51, 'tool_calls', 'Tool Calls', 'supported', 0, NULL, 10, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (52, 'responses_api', 'Responses API', 'supported', 0, NULL, 10, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (53, 'anthropic_api', 'Anthropic API', 'unsupported', 0, NULL, 10, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);
INSERT INTO `ai_model_cap` VALUES (54, 'image_understanding', '图像理解', 'unsupported', 0, NULL, 10, '2026-10-10 18:09:14', '2026-10-10 18:09:14', 1);


-- ----------------------------
-- Records of ai_model_price
-- ----------------------------
INSERT INTO `ai_model_price` VALUES (1, 1, 'input_cache_hit', 0.0200, 'off_peak', '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model_price` VALUES (2, 1, 'input_cache_hit', 0.0400, 'peak', '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model_price` VALUES (3, 1, 'input_cache_miss', 1.0000, 'off_peak', '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model_price` VALUES (4, 1, 'input_cache_miss', 2.0000, 'peak', '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model_price` VALUES (5, 1, 'output', 4.0000, 'off_peak', '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model_price` VALUES (6, 1, 'output', 8.0000, 'peak', '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model_price` VALUES (7, 2, 'input_cache_hit', 0.1500, 'off_peak', '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model_price` VALUES (8, 2, 'input_cache_hit', 0.3000, 'peak', '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model_price` VALUES (9, 2, 'input_cache_miss', 4.5000, 'off_peak', '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model_price` VALUES (10, 2, 'input_cache_miss', 9.0000, 'peak', '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model_price` VALUES (11, 2, 'output', 13.5000, 'off_peak', '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model_price` VALUES (12, 2, 'output', 27.0000, 'peak', '2026-10-10 18:03:39', '2026-10-10 18:03:39');
INSERT INTO `ai_model_price` VALUES (13, 3, 'input_cache_miss', 12.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (14, 3, 'output', 12.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (15, 4, 'input_cache_miss', 24.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (16, 4, 'output', 24.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (17, 5, 'input_cache_miss', 60.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (18, 5, 'output', 60.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (19, 6, 'input_cache_hit', 1.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (20, 6, 'input_cache_miss', 4.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (21, 6, 'output', 16.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (22, 7, 'input_cache_miss', 20.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (23, 7, 'output', 60.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (24, 8, 'input_cache_miss', 0.8000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (25, 8, 'output', 2.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (26, 9, 'input_cache_miss', 0.3000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (27, 9, 'output', 0.6000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (28, 10, 'input_cache_miss', 2.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');
INSERT INTO `ai_model_price` VALUES (29, 10, 'output', 8.0000, 'standard', '2026-10-10 18:09:14', '2026-10-10 18:09:14');

