"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SecurityScorecard/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SecurityScorecard 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:simplify。关键函数/方法:scorecardApiRequest、simplify。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SecurityScorecard/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SecurityScorecard/GenericFunctions.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function scorecardApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	query: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('securityScorecardApi');

	const headerWithAuthentication = { Authorization: `Token ${credentials.apiKey}` };

	let options: IRequestOptions = {
		headers: headerWithAuthentication,
		method,
		qs: query,
		uri: uri || `https://api.securityscorecard.io/${resource}`,
		body,
		json: true,
	};

	if (Object.keys(option).length !== 0) {
		options = Object.assign({}, options, option);
	}

	if (Object.keys(body as IDataObject).length === 0) {
		delete options.body;
	}

	if (Object.keys(query).length === 0) {
		delete options.qs;
	}
	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export function simplify(data: IDataObject[]) {
	const results = [];
	for (const record of data) {
		const newRecord: IDataObject = { date: record.date };
		for (const factor of record.factors as IDataObject[]) {
			newRecord[factor.name as string] = factor.score;
		}
		results.push(newRecord);
	}
	return results;
}
