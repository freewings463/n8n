"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/EmailSend/v2/sendAndWait.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/EmailSend/v2 的节点。导入/依赖:外部:无；内部:无；本地:./descriptions、./utils、../sendAndWait/configureWaitTillDate.util。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/EmailSend/v2/sendAndWait.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/EmailSend/v2/sendAndWait_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { fromEmailProperty, toEmailProperty } from './descriptions';
import { configureTransport } from './utils';
import { configureWaitTillDate } from '../../../utils/sendAndWait/configureWaitTillDate.util';
import {
	createEmailBodyWithN8nAttribution,
	createEmailBodyWithoutN8nAttribution,
} from '../../../utils/sendAndWait/email-templates';
import {
	createButton,
	getSendAndWaitConfig,
	getSendAndWaitProperties,
} from '../../../utils/sendAndWait/utils';

export const description: INodeProperties[] = getSendAndWaitProperties(
	[fromEmailProperty, toEmailProperty],
	'email',
);

export async function execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	const fromEmail = this.getNodeParameter('fromEmail', 0) as string;
	const toEmail = this.getNodeParameter('toEmail', 0) as string;

	const config = getSendAndWaitConfig(this);
	const buttons: string[] = [];
	for (const option of config.options) {
		buttons.push(createButton(option.url, option.label, option.style));
	}

	let htmlBody: string;

	if (config.appendAttribution !== false) {
		const instanceId = this.getInstanceId();
		htmlBody = createEmailBodyWithN8nAttribution(config.message, buttons.join('\n'), instanceId);
	} else {
		htmlBody = createEmailBodyWithoutN8nAttribution(config.message, buttons.join('\n'));
	}

	const mailOptions: IDataObject = {
		from: fromEmail,
		to: toEmail,
		subject: config.title,
		html: htmlBody,
	};

	const credentials = await this.getCredentials('smtp');
	const transporter = configureTransport(credentials, {});

	await transporter.sendMail(mailOptions);

	const waitTill = configureWaitTillDate(this);

	await this.putExecutionToWait(waitTill);
	return [this.getInputData()];
}
