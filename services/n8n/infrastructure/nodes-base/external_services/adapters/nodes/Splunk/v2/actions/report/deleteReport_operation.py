"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v2/actions/report/deleteReport.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../utils/utilities、../helpers/descriptions、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v2/actions/report/deleteReport.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v2/actions/report/deleteReport_operation.py

import type { INodeProperties, IExecuteFunctions, IDataObject } from 'n8n-workflow';

import { updateDisplayOptions } from '../../../../../utils/utilities';
import { reportRLC } from '../../helpers/descriptions';
import { splunkApiRequest } from '../../transport';

const properties: INodeProperties[] = [reportRLC];

const displayOptions = {
	show: {
		resource: ['report'],
		operation: ['deleteReport'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	i: number,
): Promise<IDataObject | IDataObject[]> {
	// https://docs.splunk.com/Documentation/Splunk/8.2.2/RESTREF/RESTsearch#saved.2Fsearches.2F.7Bname.7D

	const reportId = this.getNodeParameter('reportId', i, '', { extractValue: true }) as string;
	const endpoint = `/services/saved/searches/${reportId}`;

	await splunkApiRequest.call(this, 'DELETE', endpoint);

	return { success: true };
}
