"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/session/waitForDownload.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:无；本地:../../constants、../../GenericFunctions、../common/fields。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/session/waitForDownload.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/session/waitForDownload_operation.py

import {
	type IDataObject,
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeProperties,
} from 'n8n-workflow';

import { DEFAULT_DOWNLOAD_TIMEOUT_SECONDS } from '../../constants';
import { validateSessionId, waitForSessionEvent } from '../../GenericFunctions';
import { sessionIdField } from '../common/fields';

const displayOptions = {
	show: {
		resource: ['session'],
		operation: ['waitForDownload'],
	},
};

export const description: INodeProperties[] = [
	{
		...sessionIdField,
		displayOptions,
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions,
		options: [
			{
				displayName: 'Timeout',
				description: 'Time in seconds to wait for the download to become available',
				name: 'timeout',
				type: 'number',
				default: DEFAULT_DOWNLOAD_TIMEOUT_SECONDS,
			},
		],
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const sessionId = validateSessionId.call(this, index);
	const timeout = this.getNodeParameter(
		'timeout',
		index,
		DEFAULT_DOWNLOAD_TIMEOUT_SECONDS,
	) as number;

	// Wait for a file_status event with status 'available'
	const event = await waitForSessionEvent.call(
		this,
		sessionId,
		(sessionEvent) => sessionEvent.event === 'file_status' && sessionEvent.status === 'available',
		timeout,
	);

	// Extract fileId and downloadUrl from the event
	const result: IDataObject = {
		fileId: event.fileId,
		downloadUrl: event.downloadUrl,
	};

	return this.helpers.returnJsonArray({
		sessionId,
		data: result,
	});
}
