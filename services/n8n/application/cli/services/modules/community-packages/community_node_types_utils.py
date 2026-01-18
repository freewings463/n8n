"""
MIGRATION-META:
  source_path: packages/cli/src/modules/community-packages/community-node-types-utils.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/community-packages 的模块。导入/依赖:外部:无；内部:n8n-workflow；本地:./strapi-utils。导出:StrapiCommunityNodeType。关键函数/方法:getCommunityNodeTypes。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/community-packages/community-node-types-utils.ts -> services/n8n/application/cli/services/modules/community-packages/community_node_types_utils.py

import type { INodeTypeDescription } from 'n8n-workflow';

import { paginatedRequest } from './strapi-utils';

export type StrapiCommunityNodeType = {
	authorGithubUrl: string;
	authorName: string;
	checksum: string;
	description: string;
	displayName: string;
	name: string;
	numberOfStars: number;
	numberOfDownloads: number;
	packageName: string;
	createdAt: string;
	updatedAt: string;
	npmVersion: string;
	isOfficialNode: boolean;
	companyName?: string;
	nodeDescription: INodeTypeDescription;
	nodeVersions?: Array<{ npmVersion: string; checksum: string }>;
};

const N8N_VETTED_NODE_TYPES_STAGING_URL = 'https://api-staging.n8n.io/api/community-nodes';
const N8N_VETTED_NODE_TYPES_PRODUCTION_URL = 'https://api.n8n.io/api/community-nodes';

export async function getCommunityNodeTypes(
	environment: 'staging' | 'production',
): Promise<StrapiCommunityNodeType[]> {
	const url =
		environment === 'production'
			? N8N_VETTED_NODE_TYPES_PRODUCTION_URL
			: N8N_VETTED_NODE_TYPES_STAGING_URL;

	return await paginatedRequest<StrapiCommunityNodeType>(url);
}
