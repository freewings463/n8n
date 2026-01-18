"""
MIGRATION-META:
  source_path: packages/workflow/src/extensions/index.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/extensions 的工作流入口。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:无。用于汇总导出并完成工作流模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/extensions/index.ts -> services/n8n/domain/workflow/services/extensions/__init__.py

export {
	extend,
	extendOptional,
	hasExpressionExtension,
	hasNativeMethod,
	extendTransform,
	EXTENSION_OBJECTS as ExpressionExtensions,
} from './expression-extension';

export type {
	DocMetadata,
	NativeDoc,
	Extension,
	DocMetadataArgument,
	DocMetadataExample,
} from './extensions';

export type {
	Alias,
	AliasCompletion,
} from './extensions';
