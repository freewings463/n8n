"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/trigger/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils。导出:无。关键函数/方法:getPollResponse、prefix。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/trigger/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/trigger/GenericFunctions.py

import { NodeApiError } from 'n8n-workflow';
import type { JsonObject, IDataObject, INodeExecutionData, IPollFunctions } from 'n8n-workflow';

import { prepareFilterString, simplifyOutputMessages } from '../v2/helpers/utils';
import {
	downloadAttachments,
	microsoftApiRequest,
	microsoftApiRequestAllItems,
} from '../v2/transport';

export async function getPollResponse(
	this: IPollFunctions,
	pollStartDate: string,
	pollEndDate: string,
) {
	let responseData;
	const qs = {} as IDataObject;
	try {
		const filters = this.getNodeParameter('filters', {}) as IDataObject;
		const options = this.getNodeParameter('options', {}) as IDataObject;
		const output = this.getNodeParameter('output') as string;
		if (output === 'fields') {
			const fields = this.getNodeParameter('fields') as string[];

			if (options.downloadAttachments) {
				fields.push('hasAttachments');
			}

			qs.$select = fields.join(',');
		}

		if (output === 'simple') {
			qs.$select =
				'id,conversationId,subject,bodyPreview,from,toRecipients,categories,hasAttachments';
		}

		const filterString = prepareFilterString({ filters });

		if (filterString) {
			qs.$filter = filterString;
		}

		const endpoint = '/messages';
		if (this.getMode() !== 'manual') {
			if (qs.$filter) {
				qs.$filter = `${qs.$filter} and receivedDateTime ge ${pollStartDate} and receivedDateTime lt ${pollEndDate}`;
			} else {
				qs.$filter = `receivedDateTime ge ${pollStartDate} and receivedDateTime lt ${pollEndDate}`;
			}
			responseData = await microsoftApiRequestAllItems.call(
				this,
				'value',
				'GET',
				endpoint,
				undefined,
				qs,
			);
		} else {
			qs.$top = 1;
			responseData = await microsoftApiRequest.call(this, 'GET', endpoint, undefined, qs);
			responseData = responseData.value;
		}

		if (output === 'simple') {
			responseData = simplifyOutputMessages(responseData as IDataObject[]);
		}

		let executionData: INodeExecutionData[] = [];

		if (options.downloadAttachments) {
			const prefix = (options.attachmentsPrefix as string) || 'attachment_';
			executionData = await downloadAttachments.call(this, responseData as IDataObject[], prefix);
		} else {
			executionData = this.helpers.returnJsonArray(responseData as IDataObject[]);
		}

		return executionData;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject, {
			message: error.message,
			description: error.description,
		});
	}
}
