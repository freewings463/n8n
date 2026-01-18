"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Gmail/v2/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Gmail 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../GenericFunctions。导出:getLabels。关键函数/方法:getThreadMessages、getGmailAliases。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Gmail/v2/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Gmail/v2/loadOptions.py

import type { ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

import { googleApiRequest, getLabels } from '../GenericFunctions';

export async function getThreadMessages(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];

	const id = this.getNodeParameter('threadId', 0) as string;
	const { messages } = await googleApiRequest.call(
		this,
		'GET',
		`/gmail/v1/users/me/threads/${id}`,
		{},
		{ format: 'minimal' },
	);

	for (const message of messages || []) {
		returnData.push({
			name: message.snippet,
			value: message.id,
		});
	}

	return returnData;
}

export async function getGmailAliases(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const { sendAs } = await googleApiRequest.call(this, 'GET', '/gmail/v1/users/me/settings/sendAs');

	for (const alias of sendAs || []) {
		const displayName = alias.isDefault ? `${alias.sendAsEmail} (Default)` : alias.sendAsEmail;
		returnData.push({
			name: displayName,
			value: alias.sendAsEmail,
		});
	}

	return returnData;
}

export { getLabels };
