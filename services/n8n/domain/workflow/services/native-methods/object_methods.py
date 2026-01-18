"""
MIGRATION-META:
  source_path: packages/workflow/src/native-methods/object.methods.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/native-methods 的工作流模块。导入/依赖:外部:无；内部:无；本地:../extensions/extensions。导出:objectMethods。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/native-methods/object.methods.ts -> services/n8n/domain/workflow/services/native-methods/object_methods.py

import type { NativeDoc } from '../extensions/extensions';

export const objectMethods: NativeDoc = {
	typeName: 'Object',
	functions: {},
};
