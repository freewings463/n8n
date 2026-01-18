"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Dropcontact/GenericFunction.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Dropcontact 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:mapPairedItemsFrom。关键函数/方法:dropcontactApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Dropcontact/GenericFunction.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Dropcontact/GenericFunction.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	IPairedItemData,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';

/**
 * Make an authenticated API request to Bubble.
 */
export async function dropcontactApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject,
	qs: IDataObject,
) {
	const options: IRequestOptions = {
		method,
		uri: `https://api.dropcontact.io${endpoint}`,
		qs,
		body,
		json: true,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}

	if (!Object.keys(qs).length) {
		delete options.qs;
	}

	return await this.helpers.requestWithAuthentication.call(this, 'dropcontactApi', options);
}

export function mapPairedItemsFrom<T>(iterable: Iterable<T> | ArrayLike<T>): IPairedItemData[] {
	return Array.from(iterable, (_, i) => i).map((index) => {
		return {
			item: index,
		};
	});
}
