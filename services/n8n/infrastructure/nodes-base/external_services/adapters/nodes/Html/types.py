"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Html/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Html 的类型。导入/依赖:外部:cheerio；内部:无；本地:无。导出:Cheerio、IValueData。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Html/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Html/types.py

import type cheerio from 'cheerio';

export type Cheerio = ReturnType<typeof cheerio>;

export interface IValueData {
	attribute?: string;
	skipSelectors?: string;
	cssSelector: string;
	returnValue: string;
	key: string;
	returnArray: boolean;
}
