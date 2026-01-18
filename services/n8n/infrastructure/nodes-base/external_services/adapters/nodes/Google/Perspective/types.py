"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Perspective/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Perspective 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:CommentAnalyzeBody、Language、Comment、RequestedAttributes、AttributesValuesUi。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Perspective/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Perspective/types.py

export type CommentAnalyzeBody = {
	comment: Comment;
	requestedAttributes: RequestedAttributes;
	languages?: Language;
};

export type Language = 'de' | 'en' | 'fr' | 'ar' | 'es' | 'it' | 'pt' | 'ru';

export type Comment = {
	text?: string;
	type?: string;
};

export type RequestedAttributes = {
	[key: string]: {
		scoreType?: string;
		scoreThreshold?: {
			value: number;
		};
	};
};

export type AttributesValuesUi = {
	attributeName: string;
	scoreThreshold: number;
};
