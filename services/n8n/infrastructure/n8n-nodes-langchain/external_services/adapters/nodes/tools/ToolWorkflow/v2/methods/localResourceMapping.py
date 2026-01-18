"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/tools/ToolWorkflow/v2/methods/localResourceMapping.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/tools/ToolWorkflow 的工作流节点。导入/依赖:外部:无；内部:n8n-nodes-base/…/GenericFunctions、n8n-workflow；本地:无。导出:无。关键函数/方法:loadSubWorkflowInputs、path。用于实现 n8n 工作流节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/tools/ToolWorkflow/v2/methods/localResourceMapping.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/tools/ToolWorkflow/v2/methods/localResourceMapping.py

import { loadWorkflowInputMappings } from 'n8n-nodes-base/dist/utils/workflowInputsResourceMapping/GenericFunctions';
import type { ILocalLoadOptionsFunctions, ResourceMapperFields } from 'n8n-workflow';

export async function loadSubWorkflowInputs(
	this: ILocalLoadOptionsFunctions,
): Promise<ResourceMapperFields> {
	const { fields, subworkflowInfo, dataMode } = await loadWorkflowInputMappings.bind(this)();
	let emptyFieldsNotice: string | undefined;
	if (fields.length === 0) {
		const { triggerId, workflowId } = subworkflowInfo ?? {};
		const path = (workflowId ?? '') + (triggerId ? `/${triggerId.slice(0, 6)}` : '');
		const subworkflowLink = workflowId
			? `<a href="/workflow/${path}" target="_blank">sub-workflow’s trigger</a>`
			: 'sub-workflow’s trigger';

		switch (dataMode) {
			case 'passthrough':
				emptyFieldsNotice = `This sub-workflow is set up to receive all input data, without specific inputs the Agent will not be able to pass data to this tool. You can define specific inputs in the ${subworkflowLink}.`;
				break;
			default:
				emptyFieldsNotice = `This sub-workflow will not receive any input when called by your AI node. Define your expected input in the ${subworkflowLink}.`;
				break;
		}
	}
	return { fields, emptyFieldsNotice };
}
