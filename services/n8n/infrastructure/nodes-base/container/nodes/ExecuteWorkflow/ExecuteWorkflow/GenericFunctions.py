"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ExecuteWorkflow/ExecuteWorkflow/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ExecuteWorkflow/ExecuteWorkflow 的工作流节点。导入/依赖:外部:fs/promises；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:getWorkflowInfo。用于实现 n8n 工作流节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ExecuteWorkflow/ExecuteWorkflow/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/container/nodes/ExecuteWorkflow/ExecuteWorkflow/GenericFunctions.py

import { readFile as fsReadFile } from 'fs/promises';
import { NodeOperationError, jsonParse } from 'n8n-workflow';
import type {
	IExecuteFunctions,
	IExecuteWorkflowInfo,
	ILoadOptionsFunctions,
	INodeParameterResourceLocator,
	IRequestOptions,
} from 'n8n-workflow';

export async function getWorkflowInfo(
	this: ILoadOptionsFunctions | IExecuteFunctions,
	source: string,
	itemIndex = 0,
) {
	const workflowInfo: IExecuteWorkflowInfo = {};
	const nodeVersion = this.getNode().typeVersion;
	if (source === 'database') {
		// Read workflow from database
		if (nodeVersion === 1) {
			workflowInfo.id = this.getNodeParameter('workflowId', itemIndex) as string;
		} else {
			const { value } = this.getNodeParameter(
				'workflowId',
				itemIndex,
				{},
			) as INodeParameterResourceLocator;
			workflowInfo.id = value as string;
		}
	} else if (source === 'localFile') {
		// Read workflow from filesystem
		const workflowPath = this.getNodeParameter('workflowPath', itemIndex) as string;

		let workflowJson;
		try {
			workflowJson = await fsReadFile(workflowPath, { encoding: 'utf8' });
		} catch (error) {
			if (error.code === 'ENOENT') {
				throw new NodeOperationError(
					this.getNode(),
					`The file "${workflowPath}" could not be found, [item ${itemIndex}]`,
				);
			}

			throw error;
		}

		workflowInfo.code = jsonParse(workflowJson, {
			errorMessage: 'The file content is not valid JSON', // pass a custom error message to not expose the file contents
		});
	} else if (source === 'parameter') {
		// Read workflow from parameter
		const workflowJson = this.getNodeParameter('workflowJson', itemIndex) as string;
		workflowInfo.code = jsonParse(workflowJson);
	} else if (source === 'url') {
		// Read workflow from url
		const workflowUrl = this.getNodeParameter('workflowUrl', itemIndex) as string;

		const requestOptions = {
			headers: {
				accept: 'application/json,text/*;q=0.99',
			},
			method: 'GET',
			uri: workflowUrl,
			json: true,
			gzip: true,
		} satisfies IRequestOptions;

		const response = await this.helpers.request(requestOptions);
		workflowInfo.code = response;
	}

	return workflowInfo;
}
