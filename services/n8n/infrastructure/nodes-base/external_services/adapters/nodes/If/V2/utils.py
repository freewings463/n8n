"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/If/V2/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/If/V2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:getTypeValidationStrictness、getTypeValidationParameter。关键函数/方法:getTypeValidationStrictness、getTypeValidationParameter。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/If/V2/utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/If/V2/utils.py

import type { IExecuteFunctions } from 'n8n-workflow';

export const getTypeValidationStrictness = (version: number) => {
	return `={{ ($nodeVersion < ${version} ? $parameter.options.looseTypeValidation :  $parameter.looseTypeValidation) ? "loose" : "strict" }}`;
};

export const getTypeValidationParameter = (version: number) => {
	return (context: IExecuteFunctions, itemIndex: number, option: boolean | undefined) => {
		if (context.getNode().typeVersion < version) {
			return option;
		} else {
			return context.getNodeParameter('looseTypeValidation', itemIndex, false) as boolean;
		}
	};
};
