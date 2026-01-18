"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/transport/queryHelper.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/transport 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./requestApi、../helpers/interfaces、../helpers/utils。导出:无。关键函数/方法:theHiveApiQuery。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/transport/queryHelper.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/transport/queryHelper.py

import type { IExecuteFunctions, IDataObject } from 'n8n-workflow';

import { theHiveApiRequest } from './requestApi';
import type { QueryScope } from '../helpers/interfaces';
import { constructFilter } from '../helpers/utils';

export async function theHiveApiQuery(
	this: IExecuteFunctions,
	scope: QueryScope,
	filters?: IDataObject[],
	sortFields?: IDataObject[],
	limit?: number,
	returnCount = false,
	extraData?: string[],
) {
	const query: IDataObject[] = [];

	if (scope.id) {
		query.push({
			_name: scope.query,
			idOrName: scope.id,
		});
	} else {
		query.push({
			_name: scope.query,
		});
	}

	if (scope.restrictTo) {
		query.push({
			_name: scope.restrictTo,
		});
	}

	if (filters && Array.isArray(filters) && filters.length) {
		const filter = {
			_name: 'filter',
			_and: filters.filter((f) => f.field).map(constructFilter),
		};

		query.push(filter);
	}

	if (sortFields?.length && !returnCount) {
		const sort = {
			_name: 'sort',
			_fields: sortFields.map((field) => {
				return {
					[`${field.field as string}`]: field.direction as string,
				};
			}),
		};

		query.push(sort);
	}

	let responseData: IDataObject[] = [];

	if (returnCount) {
		query.push({
			_name: 'count',
		});

		const count = await theHiveApiRequest.call(this, 'POST', '/v1/query', { query });

		responseData.push({ count });
	} else if (limit) {
		const pagination: IDataObject = {
			_name: 'page',
			from: 0,
			to: limit,
			extraData,
		};

		query.push(pagination);
		responseData = await theHiveApiRequest.call(this, 'POST', '/v1/query', { query });
	} else {
		let to = 500;
		let from = 0;
		let response: IDataObject[] = [];

		do {
			const pagination: IDataObject = {
				_name: 'page',
				from,
				to,
				extraData,
			};

			response = await theHiveApiRequest.call(this, 'POST', '/v1/query', {
				query: [...query, pagination],
			});

			responseData = responseData.concat(response || []);
			from = to;
			to += 500;
		} while (response?.length);
	}

	return responseData;
}
