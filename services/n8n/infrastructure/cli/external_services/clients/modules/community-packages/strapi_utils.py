"""
MIGRATION-META:
  source_path: packages/cli/src/modules/community-packages/strapi-utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/community-packages 的模块。导入/依赖:外部:axios；内部:@n8n/backend-common、@n8n/di、n8n-core；本地:无。导出:Entity。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected external HTTP client usage -> infrastructure/external_services/clients
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/community-packages/strapi-utils.ts -> services/n8n/infrastructure/cli/external_services/clients/modules/community-packages/strapi_utils.py

import { Logger } from '@n8n/backend-common';
import { Container } from '@n8n/di';
import axios from 'axios';
import { ErrorReporter } from 'n8n-core';

interface ResponseData<T> {
	data: Array<Entity<T>>;
	meta: Meta;
}

interface Meta {
	pagination: Pagination;
}

export interface Entity<T> {
	id: number;
	attributes: T;
}

interface Pagination {
	page: number;
	pageSize: number;
	pageCount: number;
	total: number;
}

const REQUEST_TIMEOUT_MS = 3000;

export async function paginatedRequest<T>(url: string): Promise<T[]> {
	let returnData: T[] = [];
	let responseData: T[] | undefined = [];

	const params = {
		pagination: {
			page: 1,
			pageSize: 25,
		},
	};

	do {
		let response;
		try {
			response = await axios.get<ResponseData<T>>(url, {
				headers: { 'Content-Type': 'application/json' },
				params,
				timeout: REQUEST_TIMEOUT_MS,
			});
		} catch (error) {
			Container.get(ErrorReporter).error(error, {
				tags: { source: 'communityNodesPaginatedRequest' },
			});
			Container.get(Logger).error(
				`Error while fetching community nodes: ${(error as Error).message}`,
			);
			break;
		}

		responseData = response?.data?.data?.map((item) => item.attributes);

		if (!responseData?.length) break;

		returnData = returnData.concat(responseData);

		if (response?.data?.meta?.pagination) {
			const { page, pageCount } = response?.data.meta.pagination;

			if (page === pageCount) {
				break;
			}
		}

		params.pagination.page++;
	} while (responseData?.length);

	return returnData;
}
