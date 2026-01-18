"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Merge/v3/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Merge/v3 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./mode、./node.type、../helpers/utils。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Merge/v3/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Merge/v3/actions/router.py

import type { IExecuteFunctions } from 'n8n-workflow';

import * as mode from './mode';
import type { MergeType } from './node.type';
import { getNodeInputsData } from '../helpers/utils';

export async function router(this: IExecuteFunctions) {
	const inputsData = getNodeInputsData.call(this);
	let operationMode = this.getNodeParameter('mode', 0) as string;

	if (operationMode === 'combine') {
		const combineBy = this.getNodeParameter('combineBy', 0) as string;
		operationMode = combineBy;
	}

	return await mode[operationMode as MergeType].execute.call(this, inputsData);
}
