"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Cockpit/FormFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Cockpit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./FormInterface、./GenericFunctions。导出:无。关键函数/方法:submitForm。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Cockpit/FormFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Cockpit/FormFunctions.py

import type { IExecuteFunctions, ILoadOptionsFunctions, IDataObject } from 'n8n-workflow';

import type { IForm } from './FormInterface';
import { cockpitApiRequest } from './GenericFunctions';

export async function submitForm(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	resourceName: string,
	form: IDataObject,
) {
	const body: IForm = {
		form,
	};

	return await cockpitApiRequest.call(this, 'POST', `/forms/submit/${resourceName}`, body);
}
