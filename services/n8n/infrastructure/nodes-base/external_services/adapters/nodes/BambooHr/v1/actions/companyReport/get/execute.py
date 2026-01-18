"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/companyReport/get/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport。导出:无。关键函数/方法:get。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/companyReport/get/execute.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/companyReport/get/execute.py

import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';

import { apiRequest } from '../../../transport';

export async function get(this: IExecuteFunctions, index: number) {
	const body: IDataObject = {};
	const requestMethod = 'GET';
	const items = this.getInputData();

	//meta data
	const reportId = this.getNodeParameter('reportId', index) as string;
	const format = this.getNodeParameter('format', 0) as string;
	const fd = this.getNodeParameter('options.fd', index, true) as boolean;
	const onlyCurrent = this.getNodeParameter('options.onlyCurrent', index, true) as boolean;

	//endpoint
	const endpoint = `reports/${reportId}/?format=${format}&fd=${fd}&onlyCurrent=${onlyCurrent}`;

	if (format === 'JSON') {
		const responseData = await apiRequest.call(
			this,
			requestMethod,
			endpoint,
			body,
			{},
			{ resolveWithFullResponse: true },
		);
		return this.helpers.returnJsonArray(responseData.body as IDataObject);
	}

	const output: string = this.getNodeParameter('output', index) as string;

	const response = await apiRequest.call(this, requestMethod, endpoint, body, {} as IDataObject, {
		encoding: null,
		json: false,
		resolveWithFullResponse: true,
	});
	let mimeType = response.headers['content-type'] as string | undefined;
	mimeType = mimeType ? mimeType.split(';').find((value) => value.includes('/')) : undefined;
	const contentDisposition = response.headers['content-disposition'];
	const fileNameRegex = /(?<=filename=").*\b/;
	const match = fileNameRegex.exec(contentDisposition as string);
	let fileName = '';

	// file name was found
	if (match !== null) {
		fileName = match[0];
	}

	const newItem: INodeExecutionData = {
		json: items[index].json,
		binary: {},
	};

	if (items[index].binary !== undefined && newItem.binary) {
		// Create a shallow copy of the binary data so that the old
		// data references which do not get changed still stay behind
		// but the incoming data does not get changed.
		Object.assign(newItem.binary, items[index].binary);
	}

	newItem.binary = {
		[output]: await this.helpers.prepareBinaryData(
			response.body as unknown as Buffer,
			fileName,
			mimeType,
		),
	};

	return [newItem as unknown as INodeExecutionData[]];
}
