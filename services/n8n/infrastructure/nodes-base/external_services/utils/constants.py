"""
MIGRATION-META:
  source_path: packages/nodes-base/utils/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:NODE_RAN_MULTIPLE_TIMES_WARNING、LOCALHOST、ENABLE_LESS_STRICT_TYPE_VALIDATION。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/utils/constants.ts -> services/n8n/infrastructure/nodes-base/external_services/utils/constants.py

export const NODE_RAN_MULTIPLE_TIMES_WARNING =
	"This node ran multiple times - once for each input item. You can change this by setting 'execute once' in the node settings. <a href='https://docs.n8n.io/flow-logic/looping/#executing-nodes-once' target='_blank'>More Info</a>";

export const LOCALHOST = '127.0.0.1';

export const ENABLE_LESS_STRICT_TYPE_VALIDATION =
	"Try changing the type of comparison. Alternatively you can enable 'Convert types where required'.";
