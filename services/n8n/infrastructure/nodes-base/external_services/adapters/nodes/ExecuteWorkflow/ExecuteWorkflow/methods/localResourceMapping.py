"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ExecuteWorkflow/ExecuteWorkflow/methods/localResourceMapping.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ExecuteWorkflow/ExecuteWorkflow 的工作流节点。导入/依赖:外部:@utils/workflowInputsResourceMapping/GenericFunctions；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:loadSubWorkflowInputs、path。用于实现 n8n 工作流节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ExecuteWorkflow/ExecuteWorkflow/methods/localResourceMapping.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ExecuteWorkflow/ExecuteWorkflow/methods/localResourceMapping.py

import type { ILocalLoadOptionsFunctions, ResourceMapperFields } from 'n8n-workflow';

import { loadWorkflowInputMappings } from '@utils/workflowInputsResourceMapping/GenericFunctions';

export async function loadSubWorkflowInputs(
	this: ILocalLoadOptionsFunctions,
): Promise<ResourceMapperFields> {
	const { fields, dataMode, subworkflowInfo } = await loadWorkflowInputMappings.bind(this)();
	let emptyFieldsNotice: string | undefined;
	if (fields.length === 0) {
		const { triggerId, workflowId } = subworkflowInfo ?? {};
		const path = (workflowId ?? '') + (triggerId ? `/${triggerId.slice(0, 6)}` : '');
		const subworkflowLink = workflowId
			? `<a href="/workflow/${path}" target="_blank">sub-workflow’s trigger</a>`
			: 'sub-workflow’s trigger';

		switch (dataMode) {
			case 'passthrough':
				emptyFieldsNotice = `This sub-workflow will consume all input data passed to it. You can define specific expected input in the ${subworkflowLink}.`;
				break;
			default:
				emptyFieldsNotice = `The sub-workflow isn't set up to accept any inputs. Change this in the ${subworkflowLink}.`;
				break;
		}
	}
	return { fields, emptyFieldsNotice };
}
