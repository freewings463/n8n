"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/GSuiteAdmin/SearchFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/GSuiteAdmin 的节点。导入/依赖:外部:无；内部:无；本地:./GenericFunctions。导出:无。关键函数/方法:searchUsers、searchGroups、searchDevices。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/GSuiteAdmin/SearchFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/GSuiteAdmin/SearchFunctions.py

import type {
	ILoadOptionsFunctions,
	IDataObject,
	INodeListSearchResult,
	INodeListSearchItems,
} from 'n8n-workflow';

import { googleApiRequest, googleApiRequestAllItems } from './GenericFunctions';

export async function searchUsers(this: ILoadOptionsFunctions): Promise<INodeListSearchResult> {
	const qs: IDataObject = {
		customer: 'my_customer',
	};

	const responseData = await googleApiRequestAllItems.call(
		this,
		'users',
		'GET',
		'/directory/v1/users',
		{},
		qs,
	);

	if (!Array.isArray(responseData)) {
		return { results: [] };
	}

	const results: INodeListSearchItems[] = responseData.map(
		(user: { name?: { fullName?: string }; id: string }) => ({
			name: user.name?.fullName ?? user.id,
			value: user.id,
		}),
	);

	return { results };
}

export async function searchGroups(this: ILoadOptionsFunctions): Promise<INodeListSearchResult> {
	const qs: IDataObject = {
		customer: 'my_customer',
	};

	const responseData = await googleApiRequestAllItems.call(
		this,
		'groups',
		'GET',
		'/directory/v1/groups',
		{},
		qs,
	);

	if (!Array.isArray(responseData)) {
		return { results: [] };
	}

	const results: INodeListSearchItems[] = responseData.map(
		(group: { name?: string; email?: string; id: string }) => ({
			name: group.name || group.email || 'Unnamed Group',
			value: group.id,
		}),
	);

	return { results };
}

export async function searchDevices(this: ILoadOptionsFunctions): Promise<INodeListSearchResult> {
	const qs: IDataObject = {
		customerId: 'my_customer',
	};

	const responseData = await googleApiRequest.call(
		this,
		'GET',
		'/directory/v1/customer/my_customer/devices/chromeos/',
		{},
		qs,
	);

	if (!Array.isArray(responseData?.chromeosdevices)) {
		return { results: [] };
	}

	const results: INodeListSearchItems[] = responseData.chromeosdevices.map(
		(device: { deviceId: string; serialNumber?: string }) => ({
			name: device.serialNumber || device.deviceId || 'Unknown Device',
			value: device.deviceId,
		}),
	);

	return { results };
}
