"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v2/actions/report/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../utils/utilities、../helpers/descriptions、../helpers/utils、../../transport。导出:description。关键函数/方法:execute、searchJob。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v2/actions/report/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v2/actions/report/create_operation.py

import type { INodeProperties, IExecuteFunctions, IDataObject } from 'n8n-workflow';

import { updateDisplayOptions } from '../../../../../utils/utilities';
import { searchJobRLC } from '../../helpers/descriptions';
import { formatFeed } from '../../helpers/utils';
import { splunkApiJsonRequest, splunkApiRequest } from '../../transport';

const properties: INodeProperties[] = [
	searchJobRLC,
	{
		displayName: 'Name',
		name: 'name',
		type: 'string',
		default: '',
		description: 'The name of the report',
	},
];

const displayOptions = {
	show: {
		resource: ['report'],
		operation: ['create'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	i: number,
): Promise<IDataObject | IDataObject[]> {
	const name = this.getNodeParameter('name', i) as string;
	const searchJobId = this.getNodeParameter('searchJobId', i, '', { extractValue: true }) as string;
	const endpoint = `/services/search/jobs/${searchJobId}`;

	const searchJob = ((await splunkApiJsonRequest.call(this, 'GET', endpoint)) ?? [])[0];

	const body: IDataObject = {
		name,
		search: searchJob.search,
		alert_type: 'always',
		'dispatch.earliest_time': searchJob.earliestTime,
		'dispatch.latest_time': searchJob.latestTime,
		is_scheduled: searchJob.isScheduled,
		cron_schedule: searchJob.cronSchedule,
	};

	const returnData = await splunkApiRequest
		.call(this, 'POST', '/services/saved/searches', body)
		.then(formatFeed);

	return returnData;
}
