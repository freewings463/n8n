"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/message/sendAndWait.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:无；内部:无；本地:../helpers/utils、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/message/sendAndWait.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/actions/message/sendAndWait_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import {
	createEmailBodyWithN8nAttribution,
	createEmailBodyWithoutN8nAttribution,
} from '../../../../../../utils/sendAndWait/email-templates';
import {
	getSendAndWaitConfig,
	getSendAndWaitProperties,
	createButton,
} from '../../../../../../utils/sendAndWait/utils';
import { createMessage } from '../../helpers/utils';
import { microsoftApiRequest } from '../../transport';

export const description: INodeProperties[] = getSendAndWaitProperties([
	{
		displayName: 'To',
		name: 'toRecipients',
		description: 'Comma-separated list of email addresses of recipients',
		type: 'string',
		required: true,
		default: '',
	},
]);

export async function execute(this: IExecuteFunctions, index: number, items: INodeExecutionData[]) {
	const toRecipients = this.getNodeParameter('toRecipients', index) as string;

	const config = getSendAndWaitConfig(this);
	const buttons: string[] = [];
	for (const option of config.options) {
		buttons.push(createButton(option.url, option.label, option.style));
	}

	let bodyContent: string;
	if (config.appendAttribution !== false) {
		const instanceId = this.getInstanceId();
		bodyContent = createEmailBodyWithN8nAttribution(config.message, buttons.join('\n'), instanceId);
	} else {
		bodyContent = createEmailBodyWithoutN8nAttribution(config.message, buttons.join('\n'));
	}

	const fields: IDataObject = {
		subject: config.title,
		bodyContent,
		toRecipients,
		bodyContentType: 'html',
	};

	const message: IDataObject = createMessage(fields);

	const body: IDataObject = { message };

	await microsoftApiRequest.call(this, 'POST', '/sendMail', body);

	return items;
}
